import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './index.css'; 

const labelMap = {
  0: 'Speed Limit 20',
  1: 'Speed Limit 30',
  2: 'Speed Limit 50',
  3: 'Speed Limit 60',
  4: 'Speed Limit 70',
  5: 'Speed Limit 80',
  6: 'End of Speed Limit 80',
  7: 'Speed Limit 100',
  8: 'Speed Limit 120',
  9: 'No Passing',
  10: 'No Passing for Vehicles > 3.5 Tons',
  11: 'Right-of-Way at Intersection',
  12: 'Priority Road',
  13: 'Yield',
  14: 'Stop',
  15: 'No Vehicles',
  16: 'Vehicles > 3.5 Tons Prohibited',
  17: 'No Entry',
  18: 'General Caution',
  19: 'Dangerous Curve Left',
  20: 'Dangerous Curve Right',
  21: 'Double Curve',
  22: 'Bumpy Road',
  23: 'Slippery Road',
  24: 'Road Narrows on Right',
  25: 'Road Work',
  26: 'Traffic Signals',
  27: 'Pedestrians',
  28: 'Children Crossing',
  29: 'Bicycles Crossing',
  30: 'Beware of Ice/Snow',
  31: 'Wild Animals Crossing',
  32: 'End of All Restrictions',
  33: 'Turn Right Ahead',
  34: 'Turn Left Ahead',
  35: 'Ahead Only',
  36: 'Go Straight or Right',
  37: 'Go Straight or Left',
  38: 'Keep Right',
  39: 'Keep Left',
  40: 'Roundabout Mandatory',
  41: 'End of No Passing',
  42: 'End of No Passing for Vehicles > 3.5 Tons'
};

function App() {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState("ALL");
  const [customFilter, setCustomFilter] = useState("No Custom Filter");

  useEffect(() => {
    fetch('http://localhost:5000/detections')
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  const filteredData = data.filter(d => {
  const signNum = Number(d.sign);

  if (customFilter !== "No Custom Filter") {
    return signNum === Number(customFilter); // strict match
  }

  if (filter === "SPEED") {
    return [0, 1, 2, 3, 4, 5, 6, 7, 8].includes(signNum);
  }

  if (filter === "WARNING") {
    return [14, 15, 17, 18, 26, 29, 30, 31].includes(signNum);
  }

  return true;
});


  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 1000, background: 'white', padding: 10 }}>
        <div>
          <button className="filter-button" onClick={() => { setFilter("ALL"); setCustomFilter("No Custom Filter"); }}>All</button>
          <button className="filter-button" onClick={() => { setFilter("SPEED"); setCustomFilter("No Custom Filter"); }}>Speed</button>
          <button className="filter-button" onClick={() => { setFilter("WARNING"); setCustomFilter("No Custom Filter"); }}>Warning</button>
        </div>
        <select className="custom-dropdown" onChange={(e) => setCustomFilter(e.target.value)} value={customFilter}>
          <option value="No Custom Filter">No Custom Filter</option>
          {Object.keys(labelMap).map((key) => (
            <option key={key} value={key}>{labelMap[key]}</option>
          ))}
        </select>
      </div>

      <MapContainer center={[37.8717, -122.2682]} zoom={16} style={{ height: '100%', width: '100%' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {filteredData.map((d, i) => (
          <Marker key={i} position={[d.latitude, d.longitude]}>
            <Popup>
              <strong>{d.sign}</strong><br />
              Confidence: {Math.round(d.confidence * 100)}%<br />
              Time: {new Date(d.timestamp).toLocaleString()}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}

export default App;
