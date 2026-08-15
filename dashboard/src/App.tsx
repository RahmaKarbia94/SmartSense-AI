import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Header } from "./components/Header";
import { DevicesPage } from "./pages/DevicesPage";
import { DeviceDetailsPage } from "./pages/DeviceDetailsPage";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<DevicesPage />} />
          <Route path="/devices/:deviceId" element={<DeviceDetailsPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;