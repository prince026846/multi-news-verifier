import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Footer from "./components/Footer";
import Aboutt from "./components/Aboutt";
import HowItWorks from "./components/HowItWorks";
import Contact from "./components/Contact";

// import Dashboard from "./components/Dashboard";
// function HowItWorks() {
//   return (
//     <div className="max-w-4xl mx-auto px-6 py-12">
//       <h1 className="text-3xl font-bold mb-4">How It Works</h1>
//       <p className="text-gray-700">Step-by-step explanation coming soon!</p>
//     </div>
//   );
// }

// function Contact() {
//   return (
//     <div className="max-w-4xl mx-auto px-6 py-12">
//       <h1 className="text-3xl font-bold mb-4">Contact</h1>
//       <p className="text-gray-700">Reach us at: support@veritas.ai</p>
//     </div>
//   );
// }

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Hero />} />
          <Route path="/about" element={<Aboutt />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/contact" element={<Contact />} />
          {/* <Route path="/dashboard" element={<Dashboard />} /> */}
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
