import React from 'react';
import { Search, ShoppingCart, User, Menu } from 'lucide-react';

const PhoneFrame = ({ children }) => (
  <div className="bg-black rounded-3xl p-4 shadow-xl" style={{ width: '375px' }}>
    <div className="bg-black rounded-xl overflow-hidden">
      <div className="bg-black px-4 py-2 flex justify-center">
        <div className="w-16 h-6 bg-gray-800 rounded-full"></div>
      </div>
      <div className="bg-white" style={{ height: '812px' }}>
        {children}
      </div>
    </div>
  </div>
);

const MobileContent = () => (
  <div className="font-sans h-full flex flex-col">
    <header className="bg-blue-800 text-white p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">TriLight Homes</h1>
      <div className="flex items-center space-x-4">
        <ShoppingCart size={24} />
        <Menu size={24} />
      </div>
    </header>
    
    <div className="p-4">
      <input type="text" placeholder="Search properties..." className="w-full p-2 rounded" />
    </div>
    
    <main className="flex-grow overflow-auto p-4">
      <section className="bg-blue-600 text-white p-6 text-center rounded-lg">
        <h2 className="text-2xl font-bold mb-4">Summer Deals!</h2>
        <button className="bg-yellow-500 text-white px-6 py-3 rounded-lg text-lg font-bold w-full">
          Explore Now
        </button>
      </section>
      
      <section className="mt-6">
        <h3 className="text-lg font-bold mb-4">Shop by Category</h3>
        <div className="grid grid-cols-2 gap-4">
          {['Houses', 'Apartments', 'Condos', 'New Dev.'].map((category) => (
            <div key={category} className="bg-blue-600 text-white p-6 rounded-lg text-center">
              <p>{category}</p>
            </div>
          ))}
        </div>
      </section>
      
      <section className="mt-6">
        <h3 className="text-lg font-bold mb-4">Featured Properties</h3>
        <div className="grid grid-cols-2 gap-4">
          {[1, 2].map((product) => (
            <div key={product} className="bg-white p-4 rounded-lg shadow">
              <div className="bg-gray-200 h-32 mb-2 rounded"></div>
              <p className="font-semibold">Property {product}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
    
    <footer className="bg-blue-800 text-white p-2">
      <ul className="flex justify-around">
        <li>Home</li>
        <li>Search</li>
        <li>Saved</li>
        <li>Account</li>
      </ul>
    </footer>
  </div>
);

export default function WireframeMobileInPhone() {
  return (
    <div className="bg-gray-100 p-8 flex justify-center items-center min-h-screen">
      <PhoneFrame>
        <MobileContent />
      </PhoneFrame>
    </div>
  );
}