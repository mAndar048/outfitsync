'use client';

import Image from 'next/image';

interface Item {
  url: string;
  description: string;
}

interface ItemDisplayProps {
  items: Item[];
}

export default function ItemDisplay({ items }: ItemDisplayProps) {
  return (
    <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {items.map((item, index) => (
        <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="relative h-64">
            <Image
              src={item.url}
              alt={item.description}
              fill
              className="object-cover"
            />
          </div>
          <div className="p-4">
            <p className="text-gray-700 text-sm">{item.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
} 