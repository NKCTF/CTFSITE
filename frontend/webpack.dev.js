const config = require('./webpack.config.js');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

const distPath = path.resolve(__dirname, './public');

const dev = {
  ...config,
  devtool: 'inline-source-map',
  mode: 'development',
  plugins: [
    new CleanWebpackPlugin([distPath]),
    new HtmlWebpackPlugin({
      title: 'NKCTF',
      template: './src/index.html',
      filename: 'index.html',
    }),
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      filename: 'css/[name].ext.[hash:7].css',
      chunkFilename: 'css/[id].[hash:7].css',
    }),
  ],
};
//increase hot-reload performance
dev.module.rules.map((obj)=>{
  if(obj.test.test('.css') || obj.test.test('.vcss') || obj.test.test('.scss')) {
    obj.use = [
      'style-loader',
      'css-loader',
      'sass-loader',
    ]
  }
});
dev.resolve.alias.vue = 'vue/dist/vue.js';
dev.resolve.alias['api-config'] = path.resolve(__dirname, 'api.dev.js');

dev.output.publicPath = undefined;

module.exports = dev;
