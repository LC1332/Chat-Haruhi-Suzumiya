# CharUI

像微信一样和 AI 聊天的简洁聊天 UI 界面。

![](doc/example1.png)
![](doc/example2.png)

## 快速开始

```shell
# 安装依赖
pnpm install

# 编译 & 启动热加载开发环境
pnpm dev

# 类型检查 & 编译 & 打包为生产环境
pnpm build

# 代码格式化
pnpm lint
```

## 参与开发

### IDE 推荐

推荐使用 [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

### TS 中的 `.vue` 类型支持

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin) to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
    1) Run `Extensions: Show Built-in Extensions` from VSCode's command palette
    2) Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

### 自定义设置

See [Vite Configuration Reference](https://vitejs.dev/config/).
