"use client"

import Image from "next/image"
import { Card, CardContent, CardFooter } from "./card"
import { Button } from "./button"
import { ExternalLink } from "lucide-react"

interface Product {
  name: string
  link: string
  price: string | number
  image: string
  source: string
  thumbnail: string
  title?: string
  url?: string
  description?: string
}

interface ProductGridProps {
  products: Product[]
  isLoading?: boolean
}

export function ProductGrid({ products, isLoading = false }: ProductGridProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <Card key={i} className="animate-pulse">
            <div className="h-48 bg-muted rounded-t-lg" />
            <CardContent className="p-4">
              <div className="h-4 bg-muted rounded w-3/4 mb-2" />
              <div className="h-4 bg-muted rounded w-1/2" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (!products.length) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No products found</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {products.map((product, index) => (
        <Card key={index} className="overflow-hidden">
          <div className="relative h-48">
            <Image
              src={product.thumbnail || product.image || product.url || ""}
              alt={product.name || product.title || ""}
              fill
              className="object-cover"
            />
          </div>
          <CardContent className="p-4">
            <h3 className="font-medium line-clamp-2">{product.name || product.title}</h3>
            <p className="text-sm text-muted-foreground mt-1">
              {typeof product.price === "number"
                ? `$${product.price.toFixed(2)}`
                : product.price}
            </p>
            {product.description && (
              <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                {product.description}
              </p>
            )}
          </CardContent>
          <CardFooter className="p-4 pt-0">
            <Button
              variant="outline"
              className="w-full"
              onClick={() => window.open(product.link || product.url, "_blank")}
            >
              View Product
              <ExternalLink className="w-4 h-4 ml-2" />
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
} 