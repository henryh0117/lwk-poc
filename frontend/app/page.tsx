'use client';

import { useState, useEffect } from 'react';

const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ProductInterface {
    sku?: string;
    type1?: string;
    type2?: string;
    c_to_c?: string;
    side_a?: string;
    side_b?: string;
    side_a_bushing?: string;
    side_b_bushing?: string;
    side_a_angle?: number;
    side_b_angle?: number;
    shaft_dia?: number;
    notes?: string;
    vendor?: string;
}



interface SearchResult extends ProductInterface {
  id: number;
}

export default function Home() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<ProductInterface>({
    sku: '',
    type1: '',
    type2: '',
    c_to_c: '',
    side_a: '',
    side_b: '',
    side_a_bushing: '',
    side_b_bushing: '',
    side_a_angle: undefined,
    side_b_angle: undefined,
    shaft_dia: undefined,
    notes: '',
    vendor: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? (value ? Number(value) : undefined) : value
    }));
  };

  const handleClear = () => {
    setFormData({
      sku: '',
      type1: '',
      type2: '',
      c_to_c: '',
      side_a: '',
      side_b: '',
      side_a_bushing: '',
      side_b_bushing: '',
      side_a_angle: undefined,
      side_b_angle: undefined,
      shaft_dia: undefined,
      notes: '',
      vendor: ''
    });
  };

  useEffect(() => {
    const searchProducts = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Convert the form data to URLSearchParams, excluding empty values
        const params = new URLSearchParams();
        Object.entries(formData).forEach(([key, value]) => {
          if (value !== undefined && value !== '') {
            params.append(key, String(value));
          }
        });

        const response = await fetch(`${apiUrl}/api/products/search`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData)
        });        
        if (!response.ok) {
          throw new Error('Failed to fetch results');
        }

        const data = await response.json();
        setResults(data.products);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        setResults([]);
      } finally {
        setLoading(false);
      }
    };

    // Debounce the search
    const timeoutId = setTimeout(searchProducts, 300);

    // Cleanup function to cancel the timeout if the component unmounts
    // or if formData changes before the timeout completes
    return () => clearTimeout(timeoutId);
  }, [formData]); // Run effect when formData changes

  return (
    <div className="min-h-screen p-8">
      <main className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Cross-vendor Torque Rod Search</h1>
        <div className="flex justify-end mb-4">
          <button
            type="button"
            onClick={handleClear}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
          >
            Clear All
          </button>
        </div>
        <form className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label htmlFor="sku" className="block text-sm font-medium">SKU</label>
            <input
              type="text"
              id="sku"
              name="sku"
              className="w-full p-2 border rounded-md"
              placeholder="Enter SKU"
              value={formData.sku}
              onChange={handleInputChange}
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="type1" className="block text-sm font-medium">Type 1</label>
            <select
              id="type1"
              name="type1"
              className="w-full p-2 border rounded-md bg-white"
              value={formData.type1 || ''}
              onChange={handleInputChange}
            >
              <option value="">Select Type 1</option>
              <option value="With Bushing">With Bushing</option>
              <option value="Full Ball">Full Ball</option>
              <option value="Cabin">Cabin</option>
            </select>
          </div>

          {formData.vendor !== 'AtroBushing' && <div className="space-y-2">
            <label htmlFor="type2" className="block text-sm font-medium">Type 2</label>
            <input
              type="text"
              id="type2"
              name="type2"
              className="w-full p-2 border rounded-md"
              placeholder="Enter Type 2"
              value={formData.type2}
              onChange={handleInputChange}
            />
          </div>}

          <div className="space-y-2">
            <label htmlFor="c_to_c" className="block text-sm font-medium">Center to Center</label>
            <input
              type="text"
              id="c_to_c"
              name="c_to_c"
              className="w-full p-2 border rounded-md"
              placeholder="Enter Center to Center"
              value={formData.c_to_c}
              onChange={handleInputChange}
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="side_a" className="block text-sm font-medium">Side A</label>
            <select
              id="side_a"
              name="side_a"
              className="w-full p-2 border rounded-md bg-white"
              value={formData.side_a || ''}
              onChange={handleInputChange}
            >
              <option value="">Select Side A</option>
              <option value="Sleeve">Sleeve</option>
              <option value="Taper">Taper</option>
              <option value="Hollow">Hollow</option>
              <option value="Straddle Off">Straddle Off</option>
              <option value="N/A">N/A</option>
              <option value="4864">4864</option>
              <option value="Straddle">Straddle</option>
            </select>
          </div>

          <div className="space-y-2">
            <label htmlFor="side_b" className="block text-sm font-medium">Side B</label>
            <select
              id="side_b"
              name="side_b"
              className="w-full p-2 border rounded-md bg-white"
              value={formData.side_b || ''}
              onChange={handleInputChange}
            >
              <option value="">Select Side B</option>
              <option value="Straddle">Straddle</option>
              <option value="4865">4865</option>
              <option value="Sleeve">Sleeve</option>
              <option value="Taper">Taper</option>
              <option value="Hollow">Hollow</option>
              <option value="N/A">N/A</option>
            </select>
          </div>

          {formData.vendor !== 'AtroBushing' && <div className="space-y-2">
            <label htmlFor="side_a_bushing" className="block text-sm font-medium">Side A Bushing</label>
            <input
              type="text"
              id="side_a_bushing"
              name="side_a_bushing"
              className="w-full p-2 border rounded-md"
              placeholder="Enter Side A Bushing"
              value={formData.side_a_bushing}
              onChange={handleInputChange}
            />
          </div>}

          {formData.vendor !== 'AtroBushing' && <div className="space-y-2">
            <label htmlFor="side_b_bushing" className="block text-sm font-medium">Side B Bushing</label>
            <input
              type="text"
              id="side_b_bushing"
              name="side_b_bushing"
              className="w-full p-2 border rounded-md"
              placeholder="Enter Side B Bushing"
              value={formData.side_b_bushing}
              onChange={handleInputChange}
            />
          </div>}

          {formData.vendor !== 'AtroBushing' && <div className="space-y-2">
            <label htmlFor="side_a_angle" className="block text-sm font-medium">Side A Angle</label>
            <input
              type="text"
              id="side_a_angle"
              name="side_a_angle"
              className="w-full p-2 border rounded-md"
              placeholder="Enter Side A Angle"
              value={formData.side_a_angle || ''}
              onChange={handleInputChange}
            />
          </div>}

          {formData.vendor !== 'AtroBushing' && <div className="space-y-2">
            <label htmlFor="side_b_angle" className="block text-sm font-medium">Side B Angle</label>
            <input
              type="text"
              id="side_b_angle"
              name="side_b_angle"
              className="w-full p-2 border rounded-md"
              placeholder="Enter Side B Angle"
              value={formData.side_b_angle || ''}
              onChange={handleInputChange}
            />
          </div>}

          {formData.vendor !== 'AtroBushing' && <div className="space-y-2">
            <label htmlFor="shaft_dia" className="block text-sm font-medium">Shaft Diameter</label>
            <input
              type="text"
              id="shaft_dia"
              name="shaft_dia"
              className="w-full p-2 border rounded-md"
              placeholder="Enter Shaft Diameter"
              value={formData.shaft_dia || ''}
              onChange={handleInputChange}
            />
          </div>}

          <div className="space-y-2">
            <label htmlFor="vendor" className="block text-sm font-medium">Vendor</label>
            <select
              id="vendor"
              name="vendor"
              className="w-full p-2 border rounded-md bg-white"
              value={formData.vendor || ''}
              onChange={handleInputChange}
            >
              <option value="">Select Vendor</option>
              <option value="Automann">Automann</option>
              <option value="AtroBushing">AtroBushing</option>
            </select>
          </div>
        </form>

        <div className="mt-8">
          <h2 className="text-2xl font-semibold mb-4">{results?.length && results.length > 0 ? results.length + ' Results' : 'No results'}</h2>
          <div className="border rounded-md p-4">
            {error && (
              <p className="text-red-500">{error}</p>
            )}
            {loading ? (
              <p className="text-gray-500">Loading...</p>
            ) : results?.length && results.length > 0 ? (
              <div className="space-y-4">
                {results.map((result) => (
                  <div key={result.id} className="border p-4 rounded-md">
                    <h3 className="font-bold text-lg mb-2">{result.vendor} {result.sku}: {result.type2}</h3>
                    <div className="grid grid-cols-2 gap-2">
                      <p><span className="font-medium">Type 1:</span> {result.type1}</p>
                      <p><span className="font-medium">Type 2:</span> {result.type2}</p>
                      <p><span className="font-medium">Center to Center:</span> {result.c_to_c}</p>
                      <p><span className="font-medium">Side A:</span> {result.side_a}</p>
                      <p><span className="font-medium">Side B:</span> {result.side_b}</p>
                      {result.side_a_bushing && <p><span className="font-medium">Side A Bushing:</span> {result.side_a_bushing}</p>}
                      {result.side_b_bushing && <p><span className="font-medium">Side B Bushing:</span> {result.side_b_bushing}</p>}
                      {result.side_a_angle && <p><span className="font-medium">Side A Angle:</span> {result.side_a_angle}°</p>}
                      {result.side_b_angle && <p><span className="font-medium">Side B Angle:</span> {result.side_b_angle}°</p>}
                      {result.shaft_dia && <p><span className="font-medium">Shaft Diameter:</span> {result.shaft_dia}</p>}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No results found. Try adjusting your search criteria.</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
