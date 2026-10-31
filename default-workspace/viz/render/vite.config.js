import { defineConfig } from "vite";
import cesium from "vite-plugin-cesium";

// Static build of the TRINETRA/HIMKAVACH 3D visualization.
// vite-plugin-cesium copies Cesium's static assets (Workers/, Assets/, Widgets/).
export default defineConfig({
  base: "./",
  plugins: [cesium()],
  build: {
    outDir: "dist",
    sourcemap: false,
    chunkSizeWarningLimit: 4096,
  },
  server: { port: 5173, open: true },
});
