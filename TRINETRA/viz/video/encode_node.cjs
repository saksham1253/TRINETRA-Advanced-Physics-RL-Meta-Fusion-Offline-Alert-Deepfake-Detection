// encode_node.cjs — encode the rendered JPEG frames to H.264 MP4 entirely inside Node
// (pure WASM encoder + pure-JS JPEG decoder). No external ffmpeg binary is executed,
// because this environment blocks launching unsigned downloaded executables.
const fs = require("fs");
const path = require("path");
const jpeg = require("jpeg-js");
const HME = require("h264-mp4-encoder");

(async () => {
  const base = __dirname;
  const framesDir = path.join(base, "frames");
  const outDir = path.join(base, "output");
  fs.mkdirSync(outDir, { recursive: true });
  const files = fs.readdirSync(framesDir).filter(f => f.endsWith(".jpg")).sort();
  console.log("frames found:", files.length);

  const enc = await HME.createH264MP4Encoder();
  enc.width = 1920;
  enc.height = 1080;
  enc.frameRate = 20;
  enc.quantizationParameter = 24;   // ~10 best .. 51 worst
  enc.speed = 6;                    // 0 slow/best .. 10 fast
  enc.groupOfPictures = 40;
  enc.initialize();

  const t0 = Date.now();
  let n = 0;
  for (const f of files) {
    const buf = fs.readFileSync(path.join(framesDir, f));
    const img = jpeg.decode(buf, { useTArray: true, formatAsRGBA: true });
    enc.addFrameRgba(img.data);
    n++;
    if (n % 500 === 0) {
      const sec = (Date.now() - t0) / 1000;
      console.log(`encoded ${n}/${files.length}  (${(n / sec).toFixed(1)} fps)`);
    }
  }
  enc.finalize();
  const out = enc.FS.readFile(enc.outputFilename);
  const outPath = path.join(outDir, "trinetra_datastack.mp4");
  fs.writeFileSync(outPath, Buffer.from(out));
  enc.delete();
  console.log(`DONE ${n} frames -> ${outPath}  ${(out.length / 1048576).toFixed(1)} MB  in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
})().catch(e => { console.error("ENCODE ERROR:", e); process.exit(1); });
