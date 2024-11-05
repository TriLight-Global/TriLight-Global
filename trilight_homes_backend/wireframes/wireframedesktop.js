import React from 'react';
import { Search, User, Bell, MessageSquare, Heart, LogOut, Home, DollarSign, Key, List } from 'lucide-react';

export default function WireframeLaptopMain() {
  return (
    <div className="bg-gray-100 p-4 font-sans">
      <header className="bg-blue-600 text-white p-4 flex justify-between items-center rounded-t-lg">
        <h1 className="text-2xl font-bold">TriLight Homes</h1>
        <div className="flex-grow mx-4">
          <input type="text" placeholder="Search properties..." className="w-full p-2 rounded text-black" />
        </div>
        <nav className="flex space-x-4">
          <a href="#" className="hover:text-blue-200">Buy</a>
          <a href="#" className="hover:text-blue-200">Rent</a>
          <a href="#" className="hover:text-blue-200">Sell</a>
          <a href="#" className="hover:text-blue-200">Mortgage</a>
          <a href="#" className="hover:text-blue-200">Agents</a>
        </nav>
        <div className="flex items-center space-x-4">
          <Bell size={20} />
          <MessageSquare size={20} />
          <User size={20} />
        </div>
      </header>
      
      <main className="mt-6 bg-white rounded-lg shadow-lg p-6">
        <section className="mb-8">
          <div className="bg-blue-500 text-white p-8 rounded-lg text-center">
            <h2 className="text-3xl font-bold mb-4">Find Your Dream Home</h2>
            <div className="flex space-x-4 mb-4">
              <input type="text" placeholder="Location" className="flex-grow p-2 rounded text-black" />
              <select className="p-2 rounded text-black">
                <option>Property Type</option>
              </select>
              <select className="p-2 rounded text-black">
                <option>Price Range</option>
              </select>
              <button className="bg-yellow-500 text-white px-4 py-2 rounded">Search</button>
            </div>
          </div>
        </section>
        
        <section className="mb-8">
          <h3 className="text-xl font-bold mb-4">Featured Properties</h3>
          <div className="grid grid-cols-3 gap-6">
            {[1, 2, 3].map((property) => (
              <div key={property} className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="bg-gray-300 h-48"></div>
                <div className="p-4">
                  <h4 className="font-bold mb-2">Beautiful Home {property}</h4>
                  <p className="text-gray-600">3 bed • 2 bath • 1,500 sqft</p>
                  <p className="text-blue-600 font-bold mt-2">$350,000</p>
                </div>
              </div>
            ))}
          </div>
        </section>
        
        <section className="grid grid-cols-2 gap-6">
          <div className="bg-green-100 p-6 rounded-lg">
            <h3 className="text-xl font-bold mb-4">Market Trends</h3>
            <div className="bg-white h-64 rounded"></div>
          </div>
          <div className="bg-yellow-100 p-6 rounded-lg">
            <h3 className="text-xl font-bold mb-4">Latest Blog Posts</h3>
            <ul className="space-y-4">
              <li className="bg-white p-4 rounded">
                <h4 className="font-bold">10 Tips for First-Time Homebuyers</h4>
                <p className="text-gray-600">Read our expert advice...</p>
              </li>
              <li className="bg-white p-4 rounded">
                <h4 className="font-bold">Real Estate Market Update: Q2 2023</h4>
                <p className="text-gray-600">Get the latest insights...</p>
              </li>
            </ul>
          </div>
        </section>
      </main>
      
      <footer className="mt-8 bg-gray-800 text-white p-4 rounded-b-lg text-center">
        <p>&copy; 2023 TriLight Homes. All rights reserved.</p>
      </footer>
    </div>
  );
}