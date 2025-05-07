/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'm.media-amazon.com',
      },
      {
        protocol: 'https',
        hostname: 'images-eu.ssl-images-amazon.com',
      },
      {
        protocol: 'https',
        hostname: 'images-na.ssl-images-amazon.com',
      },
      {
        protocol: 'https',
        hostname: 'assets.myntassets.com',
      },
      {
        protocol: 'https',
        hostname: 'd118ps6mg0w7om.cloudfront.net',
      },
      {
        protocol: 'https',
        hostname: 'rukminim2.flixcart.com',
      },
      {
        protocol: 'https',
        hostname: 'rukminim3.flixcart.com',
      },
      {
        protocol: 'https',
        hostname: 'i.pinimg.com',
      },
      {
        protocol: 'https',
        hostname: 'cdn.shopify.com',
      },
      {
        protocol: 'https',
        hostname: 'www.westside.com',
      },
      {
        protocol: 'https',
        hostname: 'mirraw.com',
      },
      {
        protocol: 'https',
        hostname: 'cdn.onpointfresh.com',
      },
      {
        protocol: 'https',
        hostname: 'www.fashionbeans.com',
      },
      {
        protocol: 'https',
        hostname: 'preview.redd.it',
      },
      {
        protocol: 'https',
        hostname: 'cdnz.blacklapel.com',
      },
      {
        protocol: 'https',
        hostname: 'd1fufvy4xao6k9.cloudfront.net',
      },
      {
        protocol: 'https',
        hostname: 'www.mrporter.com',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
      }
    ],
  },
  reactStrictMode: true,
  swcMinify: true,
};

export default nextConfig;
