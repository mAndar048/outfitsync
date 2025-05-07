export interface Item {
  id: string;
  name: string;
  description: string;
  url: string;
  imageUrl?: string;  // Optional for backward compatibility
  category?: string;
} 