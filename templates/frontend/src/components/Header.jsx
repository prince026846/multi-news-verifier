import { NavLink } from "react-router-dom";

export default function Header() {
  const links = [
    { name: "Home", path: "/" },
    { name: "About", path: "/about" },
    { name: "How It Works", path: "/how-it-works" },
    { name: "Contact", path: "/contact" },
    // { name: "Dashboard", path: "/dashboard" },
  ];

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-400 to-blue-500 flex items-center justify-center text-white font-bold shadow">
            ✓
          </div>
          <div className="text-lg font-extrabold">VERITAS</div>
        </div>

        {/* Nav links */}
        <nav>
          <ul className="flex items-center gap-8 text-sm font-medium text-slate-700">
            {links.map((link) => (
              <li key={link.name}>
                <NavLink
                  to={link.path}
                  className={({ isActive }) =>
                    `py-1 transition ${
                      isActive
                        ? "text-blue-600 border-b-2 border-blue-600"
                        : "hover:text-slate-900"
                    }`
                  }
                >
                  {link.name}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
}
