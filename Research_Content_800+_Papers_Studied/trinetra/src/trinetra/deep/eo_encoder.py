"""trinetra.deep.eo_encoder — Model 4: frozen EO foundation encoder + downstream head (Class data, ws1b).

A pretrained geospatial foundation model (e.g. Prithvi / SatMAE / Clay) is used FROZEN as a feature
extractor; a small trainable head maps patch embeddings to a hazard-susceptibility / change logit. Freezing
keeps the compute inside the Kaggle budget (constraint) and avoids overfitting scarce labels. If the FM
weights are not supplied, a timm backbone is used as a transparent, clearly-labelled substitute (the chosen
encoder must be recorded for the eval report — Rule 16).
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn

from .layers import MLP


@dataclass
class EOConfig:
    backbone: str = "resnet50"      # timm name; swap for a provided FM wrapper
    in_chans: int = 6               # multispectral (e.g. S2 subset); set per dataset
    pretrained: bool = True
    freeze: bool = True
    head_hidden: tuple = (256, 64)
    n_out: int = 1


class EODownstream(nn.Module):
    """Frozen encoder + trainable MLP head. `encoder_factory` lets you inject a real FM wrapper."""

    def __init__(self, cfg: EOConfig = EOConfig(), encoder_factory=None):
        super().__init__()
        self.cfg = cfg
        if encoder_factory is not None:
            self.encoder, feat_dim = encoder_factory()
        else:
            import timm                                     # Kaggle has timm
            self.encoder = timm.create_model(
                cfg.backbone, pretrained=cfg.pretrained, in_chans=cfg.in_chans,
                num_classes=0, global_pool="avg")
            feat_dim = self.encoder.num_features
        if cfg.freeze:
            for p in self.encoder.parameters():
                p.requires_grad_(False)
        self.head = MLP([feat_dim, *cfg.head_hidden, cfg.n_out], norm=True, dropout=0.1)

    def train(self, mode: bool = True):
        super().train(mode)
        if self.cfg.freeze:
            self.encoder.eval()        # keep frozen BN stats fixed
        return self

    def forward(self, x):
        with torch.set_grad_enabled(not self.cfg.freeze):
            feats = self.encoder(x)
        logit = self.head(feats)
        return {"logit": logit, "prob": torch.sigmoid(logit)}

    def loss(self, out, targets, pos_weight=None):
        return nn.functional.binary_cross_entropy_with_logits(
            out["logit"].squeeze(-1), targets.float(), pos_weight=pos_weight)
