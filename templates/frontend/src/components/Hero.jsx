import globe from "./images.png";
import pattern from "./abstact.jpg";

export default function Hero() {
  return (
    <section className="max-w-7xl mx-auto px-6 mt-8">
      {/* Card */}
      <div className="relative rounded-2xl overflow-hidden shadow-2xl">
        {/* background pattern */}
        <img
          src={pattern}
          alt="pattern"
          className="absolute inset-0 w-full h-full object-cover opacity-30 blur-sm pointer-events-none"
        />

        {/* dark overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-[#0b1c2a]/95 via-[#0b1c2a]/80 to-transparent pointer-events-none"></div>

        {/* content */}
        <div className="relative z-10 px-6 py-12 md:py-20 md:px-14 grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
          {/* left text */}
          <div className="text-white">
            <h1 className="text-4xl md:text-6xl font-extrabold leading-tight tracking-wide drop-shadow-lg">
              SEEK{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500">
                TRUTH
              </span>{" "}
              IN A
              <br />
              NOISY WORLD
            </h1>

            <p className="mt-4 text-lg text-sky-100/90 max-w-xl leading-relaxed">
              Verify News Across All Platforms, Instantly.
            </p>

            <div className="mt-8 flex items-center gap-4">
              <a
                href="http://127.0.0.1:5000/"
                className="bg-gradient-to-r from-blue-500 to-green-400 hover:opacity-95 text-white font-semibold px-8 py-3 rounded-full shadow-xl transition-transform transform hover:scale-105 hover:shadow-green-400/40"
              >
                Start Verifying
              </a>

              <button className="px-6 py-3 rounded-full border border-white/30 text-white/90 hover:bg-white/10 hover:scale-105 transition-transform">
                Learn how
              </button>
            </div>
          </div>

          {/* right globe image */}
          <div className="flex justify-center md:justify-end">
            <div className="relative w-72 md:w-96 animate-bounce-slow">
              {/* glowing aura */}
              <div className="absolute inset-0 rounded-full bg-gradient-to-br from-green-400/40 to-blue-500/40 blur-2xl"></div>
              <img
                src={globe}
                alt="globe"
                className="relative w-full h-auto rounded-full drop-shadow-2xl border-4 border-transparent bg-gradient-to-r from-green-400 to-blue-500 p-1"
              />
            </div>
          </div>
        </div>

        {/* subtle bottom shadow */}
        <div className="pointer-events-none absolute -bottom-6 left-8 right-8 h-6 rounded-b-2xl bg-gradient-to-t from-black/20 to-transparent blur-sm opacity-60"></div>
      </div>
    </section>
  );
}
