import { useState, useEffect } from 'react';
import AirportDropdown from './components/AirportDropdown';

type Airport = {
  airport: string;
  city: string;
};

function App() {
  const [airports, setAirports] = useState<Airport[]>([]);
  const [departure, setDeparture] = useState<Airport | null>(null);
  const [destination, setDestination] = useState<Airport | null>(null);
  const [month, setMonth] = useState<number | null>(null);
  const [fare, setFare] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/airports')
      .then(response => response.json())
      .then(data => setAirports(data.airports))
      .catch(error => console.error('Error fetching airports:', error));
  }, []);

  const availableDepartures = destination
    ? airports.filter((a) => a.airport !== destination.airport)
    : airports;

  const availableDestinations = departure
    ? airports.filter((a) => a.airport !== departure.airport)
    : airports;

  const handlePredict = async () => {
    if (!departure || !destination || !month) {
      alert("Please select origin, destination, and month.");
      return;
    }

    setLoading(true);
    setFare(null);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          origin: departure.airport,
          dest: destination.airport,
          month: month
        })
      });

      const data = await response.json();
      setFare(data.fare);
    } catch (error) {
      console.error('Error predicting fare:', error);
      alert('Failed to fetch fare.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen bg-gradient-to-r from-purple-400 via-pink-500 to-red-500">
      <div className="flex items-center justify-center h-full">
        <div className="bg-white p-6 rounded-lg shadow-lg max-w-xl w-full text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Flight Fare Predictor</h2>

          <div className="flex justify-center space-x-4 mb-4">
            <div>
              <label className="block text-gray-600 mb-1">Departure</label>
              <AirportDropdown
                airports={availableDepartures}
                selected={departure}
                onSelect={setDeparture}
              />
            </div>
            <div>
              <label className="block text-gray-600 mb-1">Destination</label>
              <AirportDropdown
                airports={availableDestinations}
                selected={destination}
                onSelect={setDestination}
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-gray-600 mb-1">Month</label>
            <select
              className="px-4 py-2 rounded-md bg-gray-200"
              value={month ?? ''}
              onChange={(e) => setMonth(Number(e.target.value) || null)}
            >
              <option value="">Select Month</option>
              {[...Array(12)].map((_, i) => (
                <option key={i + 1} value={i + 1}>
                  {new Date(0, i).toLocaleString('default', { month: 'long' })}
                </option>
              ))}
            </select>
          </div>

          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            onClick={handlePredict}
            disabled={loading}
          >
            {loading ? 'Predicting...' : 'Get Fare'}
          </button>

          {fare !== null && (
            <div className="mt-6 text-xl text-green-700 font-semibold">
              Predicted Fare: ${fare.toFixed(2)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
