export default function Contact() {
  return (
    <section className="bg-gray-50 py-16">
      <div className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
        {/* Left side - Form */}
        <div>
          <h1 className="text-4xl font-extrabold text-gray-900 mb-6">
            Contact Us
          </h1>
          <p className="text-gray-600 mb-8">
            Have questions or feedback? We'd love to hear from you. Fill out the
            form below or reach us directly.
          </p>

          <form className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Name
              </label>
              <input
                type="text"
                placeholder="Your Name"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                placeholder="your@email.com"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Message
              </label>
              <textarea
                rows="5"
                placeholder="Write your message..."
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              ></textarea>
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-500 to-green-400 text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:opacity-90 transition"
            >
              Send Message
            </button>
          </form>
        </div>

        {/* Right side - Contact Info + Map */}
        <div className="bg-white rounded-2xl shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Get in Touch
          </h2>
          <ul className="space-y-4 text-gray-600 mb-8">
            <li>
              📧 <span className="ml-2">support@veritas.ai</span>
            </li>
            <li>
              📞 <span className="ml-2">+1 (234) 567-890</span>
            </li>
            <li>
              📍 <span className="ml-2">123 News Lane, Info City, World</span>
            </li>
          </ul>

          {/* Map Illustration */}
          <div className="w-full h-48 bg-gray-100 rounded-lg overflow-hidden flex items-center justify-center">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Globe_icon.svg/512px-Globe_icon.svg.png"
              alt="Map"
              className="w-32 h-32 opacity-80"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
