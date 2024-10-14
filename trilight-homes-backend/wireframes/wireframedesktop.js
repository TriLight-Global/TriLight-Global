import React from 'react';
import { Search, ShoppingCart, User } from 'lucide-react';

export default function WireframeDesktop() {
  return (
    <div className="bg-gray-100 p-4 font-sans">
      <header className="bg-blue-800 text-white p-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">TriLight Homes</h1>
        <div className="flex-grow mx-4">
          <input type="text" placeholder="Search properties..." className="w-full p-2 rounded text-black" />
        </div>
        <div className="flex items-center space-x-4">
          <button className="bg-yellow-500 text-white px-4 py-2 rounded flex items-center">
            <ShoppingCart size={20} className="mr-2" />
            Saved (3)
          </button>
          <button className="bg-white text-blue-800 px-4 py-2 rounded">Login</button>
        </div>
      </header>
      
      <nav className="bg-blue-700 text-white p-2">
        <ul className="flex space-x-6">
          <li>Home</li>
          <li>Buy</li>
          <li>Rent</li>
          <li>Sell</li>
          <li>Mortgage</li>
          <li>Agent Finder</li>
        </ul>
      </nav>
      
      <main className="mt-6">
        <section className="bg-blue-600 text-white p-8 text-center rounded-lg">
          <h2 className="text-3xl font-bold mb-4">Summer Deals: Up to 20% Off!</h2>
          <button className="bg-yellow-500 text-white px-6 py-3 rounded-lg text-xl font-bold">
            Explore Now
          </button>
        </section>
        
        <section className="mt-8">
          <h3 className="text-xl font-bold mb-4">Shop by Category</h3>
          <div className="grid grid-cols-4 gap-4">
            {['Houses', 'Apartments', 'Condos', 'New Developments'].map((category) => (
              <div key={category} className="bg-blue-600 text-white p-8 rounded-lg text-center">
                <p className="text-xl">{category}</p>
              </div>
            ))}
          </div>
        </section>
        
        <section className="mt-8">
          <h3 className="text-xl font-bold mb-4">Featured Properties</h3>
          <div className="grid grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((product) => (
              <div key={product} className="bg-white p-4 rounded-lg shadow">
                <div className="bg-gray-200 h-40 mb-2 rounded"></div>
                <p className="font-semibold">Property {product}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}