module.exports = {
  configureWebpack: {
    devtool: 'source-map',
    plugins: [],
  },
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === 'production' ? './dist' : '/',
  outputDir: '../lyrebird_api_coverage/dist',
  devServer: {
    proxy: 'http://localhost:9090',
  },
}
