import prettierConfig from "eslint-config-prettier/flat";
import pluginVue from "eslint-plugin-vue";
import vueParser from "vue-eslint-parser";
import tseslint from "typescript-eslint";
import globals from "globals";

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    ignores: ["**/.nuxt", "**/node_modules", "**/.output", "**/dist", "eslint.config.js"]
  },
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node }
    }
  },
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  ...pluginVue.configs["flat/recommended"],
  prettierConfig,
  {
    name: "main",
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tseslint.parser,
        extraFileExtensions: [".vue"],
        projectService: true,
        tsconfigRootDir: import.meta.dirname
      }
    }
  },
  {
    rules: {
      "array-callback-return": ["warn", { allowImplicit: true }],
      curly: ["warn", "multi-line"],
      "id-length": ["warn", { exceptions: ["a", "b", "_"] }], // .sort() and route queries
      "no-template-curly-in-string": "warn",
      "no-unreachable-loop": "warn",
      "no-use-before-define": "warn",
      "block-scoped-var": "warn",
      camelcase: "warn",
      complexity: "warn",
      "default-case": "warn",
      "default-case-last": "warn",
      eqeqeq: "warn",
      "func-style": ["warn", "declaration"],
      "max-depth": "warn",
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "no-else-return": "warn",
      "no-empty-function": "warn",
      "no-lonely-if": "warn",
      "no-unneeded-ternary": "warn",
      "no-unused-expressions": "warn",
      "no-useless-computed-key": "warn",
      "no-useless-concat": "warn",
      "no-useless-return": "warn",
      "no-var": "warn",
      "operator-assignment": "warn",
      "prefer-arrow-callback": "warn",
      "prefer-const": "warn",
      "prefer-object-has-own": "warn",
      "prefer-object-spread": "warn",
      "prefer-template": "warn",
      yoda: "warn",

      "@typescript-eslint/consistent-type-definitions": ["warn"],
      "@typescript-eslint/array-type": "warn",
      "default-param-last": "off",
      "@typescript-eslint/default-param-last": "warn",
      "dot-notation": "off",
      "@typescript-eslint/dot-notation": "warn",
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          args: "all",
          argsIgnorePattern: "^_",
          caughtErrors: "all",
          caughtErrorsIgnorePattern: "^_",
          destructuredArrayIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          ignoreRestSiblings: true
        }
      ],

      "@typescript-eslint/no-confusing-void-expression": "off",
      "@typescript-eslint/no-explicit-any": "off",
      "@typescript-eslint/no-invalid-void-type": "off",
      "@typescript-eslint/no-unnecessary-condition": "off",
      "@typescript-eslint/no-unnecessary-type-assertion": "off",
      "@typescript-eslint/no-unnecessary-type-parameters": "off",
      "@typescript-eslint/no-unsafe-argument": "off",
      "@typescript-eslint/no-unsafe-assignment": "off",
      "@typescript-eslint/no-unsafe-call": "off",
      "@typescript-eslint/no-unsafe-member-access": "off",
      "@typescript-eslint/no-unsafe-return": "off",
      "@typescript-eslint/restrict-template-expressions": "off",
      "@typescript-eslint/no-redundant-type-constituents": "off",
      "@typescript-eslint/restrict-plus-operands": "off",
      "@typescript-eslint/unified-signatures": "off",

      "vue/attributes-order": [
        "warn",
        {
          order: ["DEFINITION", "CONDITIONALS", "LIST_RENDERING", "RENDER_MODIFIERS", "GLOBAL", ["UNIQUE", "SLOT"], "TWO_WAY_BINDING", "OTHER_DIRECTIVES", "OTHER_ATTR", "EVENTS", "CONTENT"],
          alphabetical: false
        }
      ],
      "vue/block-lang": ["warn", { script: { lang: "ts" } }],
      "vue/block-order": ["warn", { order: ["template", "script", "style"] }],
      "vue/component-api-style": "warn",
      "vue/component-name-in-template-casing": "warn",
      "vue/custom-event-name-casing": "warn",
      "vue/define-emits-declaration": "warn",
      "vue/define-props-declaration": "warn",
      "vue/enforce-style-attribute": "warn",
      "vue/html-button-has-type": "warn",
      "vue/new-line-between-multi-line-property": "warn",
      "vue/no-mutating-props": "off",
      "vue/no-static-inline-styles": "warn",
      "vue/no-template-target-blank": "warn",
      "vue/no-unused-emit-declarations": "warn",
      "vue/no-unused-properties": "warn",
      "vue/no-unused-refs": "warn",
      "vue/no-useless-mustaches": "warn",
      "vue/no-useless-v-bind": "warn",
      "vue/padding-line-between-blocks": "warn",
      "vue/prefer-use-template-ref": "warn",
      "vue/require-typed-object-prop": "warn",
      "vue/v-for-delimiter-style": "warn",
      "vue/dot-notation": "warn",
      "vue/camelcase": "warn",
      "vue/no-console": "warn",
      "vue/no-constant-condition": "warn",
      "vue/no-v-html": "warn",

      "vue/no-use-v-if-with-v-for": "off",
      "vue/multi-word-component-names": "off",
      "vue/html-self-closing": ["warn", { html: { void: "always", normal: "never", component: "always" } }],
      "vue/max-attributes-per-line": "off",
      "vue/require-v-for-key": "off",
      "vue/singleline-html-element-content-newline": "off",
      "vue/multiline-html-element-content-newline": "off"
    }
  }
];
