// src/App.tsx
import React from 'react';
import RfidForm from './components/RfidForm';
import RfidTable from './components/RfidTable';

const App: React.FC = () => {
  return (
    <div>
      <h1>RFID Tracking System</h1>
      <RfidForm />
      <RfidTable />
    </div>
  );
};

export default App;
