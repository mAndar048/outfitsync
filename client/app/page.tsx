"use client";

import { useState } from "react";
import Navigation from '@/components/Navigation';
import ImageUpload from '@/components/ImageUpload';
import ItemDisplay from '@/components/ItemDisplay';
import { Item } from '@/lib/types';

export default function Home() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <main className="min-h-screen bg-gray-50">
      <Navigation />
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg p-6">
            <ImageUpload
              onImagesChange={() => {}} // Empty function since we don't use files state anymore
              onItemsGenerated={setItems}
              setLoading={setLoading}
              setError={setError}
            />
            {loading && (
              <div className="mt-4 flex justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-900"></div>
              </div>
            )}
            {error && (
              <div className="mt-4 text-red-600 text-center">{error}</div>
            )}
            {items.length > 0 && <ItemDisplay items={items} />}
          </div>
        </div>
      </div>
    </main>
  );
}

// Add this to your global CSS or create a new animation
// tailwind.config.js:
// extend: {
//   keyframes: {
//     fadeIn: {
//       '0%': { opacity: '0', transform: 'translateY(10px)' },
//       '100%': { opacity: '1', transform: 'translateY(0)' }
//     }
//   },
//   animation: {
//     fadeIn: 'fadeIn 0.5s ease-out forwards'
//   }
// }
