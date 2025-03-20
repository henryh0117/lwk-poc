/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // Enable if you need to access the backend API
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/:path*',
  //       destination: 'http://backend:8000/:path*',
  //     },
  //   ]
  // },
}

module.exports = nextConfig
