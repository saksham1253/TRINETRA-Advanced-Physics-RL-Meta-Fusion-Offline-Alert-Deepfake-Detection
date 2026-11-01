// encode720.cjs — encode the 720p frames to a compact H.264 MP4 inside Node (pure WASM; no ffmpeg).
const fs = require("fs");
const path = require("path");
const jpeg = require("jpeg-js");
const HME = require("h264-mp4-encoder");

(async () => {
  const base = __dirname;
  const framesDir = path.join(base, "frames720");
  const outPath = path.join(base, "output", "trinetra_datastack_720.mp4");
  const files = fs.readdirSync(framesDir).filter(f => f.endsWith(".jpg")).sort();
  console.log("frames:", files.length);
  const enc = await HME.createH264MP4Encoder();
  enc.width = 1280; enc.height = 720; enc.frameRate = 20;
  enc.quantizationParameter = 29;   // compact
  enc.speed = 8;                    // fast
  enc.groupOfPictures = 60;
  enc.initialize();
  const t0 = Date.now();
  let n = 0;
  for (const f of files) {
    const img = jpeg.decode(fs.readFileSync(path.join(framesDir, f)), { useTArray: true, formatAsRGBA: true });
    enc.addFrameRgba(img.data);
    if (++n % 500 === 0) console.log(`enc ${n}/${files.length}  ${(n/((Date.now()-t0)/1000)).toFixed(1)} fps`);
  }
  enc.finalize();
  const out = enc.FS.readFile(enc.outputFilename);
  fs.writeFileSync(outPath, Buffer.from(out));
  enc.delete();
  console.log(`DONE -> ${outPath}  ${(out.length/1048576).toFixed(1)} MB in ${((Date.now()-t0)/1000).toFixed(0)}s`);
})().catch(e => { console.error("ERR", e); process.exit(1); });
