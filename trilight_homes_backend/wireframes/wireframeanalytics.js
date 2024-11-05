import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

const propertyData = [
  { name: 'Jan', sales: 4000, rentals: 2400 },
  { name: 'Feb', sales: 3000, rentals: 1398 },
  { name: 'Mar', sales: 2000, rentals: 9800 },
  { name: 'Apr', sales: 2780, rentals: 3908 },
  { name: 'May', sales: 1890, rentals: 4800 },
  { name: 'Jun', sales: 2390, rentals: 3800 },
];

const marketTrends = [
  { name: 'Jan', price: 2400 },
  { name: 'Feb', price: 2210 },
  { name: 'Mar', price: 2290 },
  { name: 'Apr', price: 2000 },
  { name: 'May', price: 2181 },
  { name: 'Jun', price: 2500 },
];

const propertyTypes = [
  { name: 'Houses', value: 400 },
  { name: 'Apartments', value: 300 },
  { name: 'Condos', value: 200 },
  { name: 'Townhouses', value: 100 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export default function WireframeLaptopAnalytics() {
  return (
    <div className="bg-gray-100 p-4 font-sans">
      <header className="bg-blue-600 text-white p-4 flex justify-between items-center rounded-t-lg">
        <h1 className="text-2xl font-bold">TriLight Homes Analytics</h1>
        <nav className="flex space-x-4">
          <a href="#" className="hover:text-blue-200">Dashboard</a>
          <a href="#" className="hover:text-blue-200">Properties</a>
          <a href="#" className="hover:text-blue-200">Market</a>
          <a href="#" className="hover:text-blue-200">Reports</a>
        </nav>
      </header>
      
      <main className="mt-6 bg-white rounded-lg shadow-lg p-6">
        <div className="grid grid-cols-2 gap-6 mb-6">
          <section className="bg-blue-100 rounded-lg p-4">
            <h2 className="text-xl font-semibold mb-4">Property Transactions</h2>
            <BarChart width={500} height={300} data={propertyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="sales" fill="#8884d8" />
              <Bar dataKey="rentals" fill="#82ca9d" />
            </BarChart>
          </section>
          
          <section className="bg-green-100 rounded-lg p-4">
            <h2 className="text-xl font-semibold mb-4">Market Trends</h2>
            <LineChart width={500} height={300} data={marketTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="price" stroke="#8884d8" />
            </LineChart>
          </section>
        </div>
        
        <div className="grid grid-cols-2 gap-6">
          <section className="bg-yellow-100 rounded-lg p-4">
            <h2 className="text-xl font-semibold mb-4">Property Types</h2>
            <PieChart width={400} height={300}>
              <Pie
                data={propertyTypes}
                cx={200}
                cy={150}
                innerRadius={60}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
              >
                {propertyTypes.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </section>
          
          <section className="bg-purple-100 rounded-lg p-4">
            <h2 className="text-xl font-semibold mb-4">Key Metrics</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white p-4 rounded shadow">
                <h3 className="text-lg font-semibold">Total Properties</h3>
                <p className="text-3xl font-bold text-blue-600">1,234</p>
              </div>
              <div className="bg-white p-4 rounded shadow">
                <h3 className="text-lg font-semibold">Avg. Sale Price</h3>
                <p className="text-3xl font-bold text-green-600">$350,000</p>
              </div>
              <div className="bg-white p-4 rounded shadow">
                <h3 className="text-lg font-semibold">Active Listings</h3>
                <p className="text-3xl font-bold text-yellow-600">567</p>
              </div>
              <div className="bg-white p-4 rounded shadow">
                <h3 className="text-lg font-semibold">Avg. Days on Market</h3>
                <p className="text-3xl font-bold text-purple-600">45</p>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}