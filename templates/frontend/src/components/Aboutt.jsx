export default function About() {
  return (
    <section className="max-w-5xl mx-auto px-6 py-16">
      {/* Title */}
      <h1 className="text-4xl font-extrabold text-center text-gray-900 mb-6">
        About This Project
      </h1>

      {/* Description */}
      <p className="text-center text-lg text-gray-600 max-w-3xl mx-auto mb-12 leading-relaxed">
        <span className="font-semibold">Multi-Media News Verifier</span> is an
        AI-powered platform that helps you quickly check whether news is fake or
        real. It supports multiple languages, making verification accessible to
        everyone, and ensures results are backed by trusted sources.
      </p>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-10">
        {/* Card 1 */}
        <div className="p-6 bg-white rounded-2xl shadow-md hover:shadow-lg transition">
          <div className="flex justify-center mb-4">
            <div className="bg-blue-100 text-blue-600 w-14 h-14 flex items-center justify-center rounded-full text-2xl font-bold">
              ⚡
            </div>
          </div>
          <h3 className="text-xl font-semibold text-center">
            Fast Verification
          </h3>
          <p className="text-gray-600 text-center mt-2">
            Instantly analyze news across text, images, audio, and more.
          </p>
        </div>

        {/* Card 2 */}
        <div className="p-6 bg-white rounded-2xl shadow-md hover:shadow-lg transition">
          <div className="flex justify-center mb-4">
            <div className="bg-green-100 text-green-600 w-14 h-14 flex items-center justify-center rounded-full text-2xl font-bold">
              🌐
            </div>
          </div>
          <h3 className="text-xl font-semibold text-center">
            Local Language Support
          </h3>
          <p className="text-gray-600 text-center mt-2">
            Verify news in your own language with AI-powered translations.
          </p>
        </div>

        {/* Card 3 */}
        <div className="p-6 bg-white rounded-2xl shadow-md hover:shadow-lg transition">
          <div className="flex justify-center mb-4">
            <div className="bg-purple-100 text-purple-600 w-14 h-14 flex items-center justify-center rounded-full text-2xl font-bold">
              🔒
            </div>
          </div>
          <h3 className="text-xl font-semibold text-center">Trusted Sources</h3>
          <p className="text-gray-600 text-center mt-2">
            Results are backed by verified and reliable information sources.
          </p>
        </div>
      </div>
    </section>
  );
}
