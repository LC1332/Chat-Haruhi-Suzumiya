import {
  defineConfig,
  presetUno,
  presetTypography,
  presetIcons,
  transformerDirectives,
} from "unocss";

export default defineConfig({
  presets: [presetUno(), presetTypography(), presetIcons()],
  transformers: [transformerDirectives()],
});
