import { fileURLToPath, URL } from "node:url";

import UnoCSS from "unocss/vite";
import Icons from "unplugin-icons/vite";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import {
  AntDesignVueResolver,
  ElementPlusResolver,
} from "unplugin-vue-components/resolvers";
import IconsResolver from "unplugin-icons/resolver";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    UnoCSS(),
    Icons(),
    AutoImport({
      imports: ["vue", "vue-router", "@vueuse/core"],
      resolvers: [ElementPlusResolver(), AntDesignVueResolver()],
      dts: true,
      eslintrc: {
        enabled: true,
      },
    }),
    Components({
      resolvers: [
        ElementPlusResolver(),
        AntDesignVueResolver({ importStyle: false }),
        IconsResolver(),
      ],
      dts: true,
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
