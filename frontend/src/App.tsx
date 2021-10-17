import React from "react";
import { WorkoutsForward } from "components/WorkoutsForward";

const App: React.FC = () => {
  return (
    <div className="container mx-auto">
      <h1 className="text-6xl">uOttawa Gym Demand</h1>
      <WorkoutsForward />
    </div>
  );
};

export default App;
