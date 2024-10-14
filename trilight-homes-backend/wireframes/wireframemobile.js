import React from 'react';
import { Search, Home, Heart, MessageSquare, User, MapPin, Bath, Bed, Move, Star, ChevronRight } from 'lucide-react';

const SmartphoneFrame = ({ children }) => (
  <div className="bg-gray-900 w-[375px] h-[812px] rounded-[60px] shadow-xl overflow-hidden relative">
    <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-40 h-7 bg-black rounded-b-3xl"></div>
    <div className="absolute top-2 left-1/2 transform -translate-x-1/2 w-20 h-1 bg-gray-800 rounded-full"></div>
    <div className="bg-white h-full w-full pt-12 pb-8 px-4 overflow-y-auto">
      {children}
    </div>
    <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 w-40 h-1 bg-gray-800 rounded-full"></div>
  </div>
);

const PropertyCard = ({ title, price, beds, baths, area, image }) => (
  <div className="bg-white rounded-xl shadow-md overflow-hidden mb-4">
    <div className="relative">
      <img src={image} alt={title} className="w-full h-48 object-cover" />
      <div className="absolute top-2 right-2 bg-white rounded-full p-2">
        <Heart size={20} className="text-red-500" />
      </div>
    </div>
    <div className="p-4">
      <h3 className="font-bold text-lg mb-2">{title}</h3>
      <p className="text-blue-600 font-bold text-xl mb-2">{price}</p>
      <div className="flex justify-between text-gray-600">
        <span className="flex items-center"><Bed size={16} className="mr-1" /> {beds} beds</span>
        <span className="flex items-center"><Bath size={16} className="mr-1" /> {baths} baths</span>
        <span className="flex items-center"><Move size={16} className="mr-1" /> {area} sqft</span>
      </div>
    </div>
  </div>
);

export default function DetailedMobileWireframe() {
  return (
    <div className="bg-gray-100 p-8 flex justify-center items-center min-h-screen">
      <SmartphoneFrame>
        <header className="bg-blue-600 text-white p-4 rounded-t-3xl mb-4">
          <h1 className="text-xl font-bold mb-2">TriLight Homes</h1>
          <div className="relative">
            <input 
              type="text" 
              placeholder="Search properties..." 
              className="w-full p-2 pl-10 rounded-full text-gray-800"
            />
            <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" />
          </div>
        </header>
        
        <section className="mb-6">
          <h2 className="text-2xl font-bold mb-4">Discover Properties</h2>
          <div className="flex space-x-4 mb-4 overflow-x-auto pb-2">
            {['Houses', 'Apartments', 'Condos', 'Villas'].map((category) => (
              <div key={category} className="flex-shrink-0 bg-blue-100 text-blue-800 px-4 py-2 rounded-full">
                {category}
              </div>
            ))}
          </div>
        </section>
        
        <section className="mb-6">
          <h2 className="text-2xl font-bold mb-4">Featured Listings</h2>
          <PropertyCard 
            title="Modern Downtown Apartment" 
            price="$425,000" 
            beds="2" 
            baths="2" 
            area="1,200" 
            image="/api/placeholder/400/300"
          />
          <PropertyCard 
            title="Cozy Suburban Home" 
            price="$550,000" 
            beds="3" 
            baths="2.5" 
            area="1,800" 
            image="/api/placeholder/400/300"
          />
        </section>
        
        <section className="mb-6">
          <h2 className="text-2xl font-bold mb-4">Explore Neighborhoods</h2>
          <div className="bg-gray-200 rounded-xl p-4 flex items-center justify-between">
            <div className="flex items-center">
              <MapPin size={24} className="text-blue-600 mr-3" />
              <div>
                <h3 className="font-bold">Downtown</h3>
                <p className="text-sm text-gray-600">86 listings</p>
              </div>
            </div>
            <ChevronRight size={24} className="text-gray-400" />
          </div>
        </section>
        
        <section>
          <h2 className="text-2xl font-bold mb-4">Market Insights</h2>
          <div className="bg-blue-100 rounded-xl p-4">
            <h3 className="font-bold mb-2">Property Price Trends</h3>
            <p className="text-sm text-gray-600 mb-4">Prices up 5% this quarter</p>
            <div className="h-40 bg-white rounded-lg"></div>
          </div>
        </section>
      </SmartphoneFrame>
    </div>
  );
}