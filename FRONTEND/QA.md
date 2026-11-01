# QA checklist (status 2026-11-01)
- [x] Golden tests pass (8) · [x] scenario determinism (8) · [x] live contract (2) · [x] typecheck · [x] production build
- [x] Every slider comes from the registry; unresolved repo refs fail the extractor
- [x] Mode chip and prototype badge in the top bar on every screen; origin chip on every alert card
- [x] Approval gate; dispatch is a no-op with "DEMO: no message sent"
- [x] Severity encoded by shape + colour + label; pulses at 0.6 Hz (< 3 Hz); reduce-motion setting
- [ ] Browser walk-through of the six screens at 1920×1080 and 1366×768 (not done: no browser in this sandbox)
- [ ] Offline test with network disabled · [ ] fps measurement · [ ] Playwright screenshots (dark/light × 3 languages)
- [ ] Hindi strings reviewed by a native speaker · [ ] colour-blind and projector simulation
