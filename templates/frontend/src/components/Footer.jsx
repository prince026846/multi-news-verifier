export default function Footer() {
  return (
    <footer className="bg-white mt-10">
      <div className="max-w-7xl mx-auto px-6 py-6 text-center text-slate-600">
        <p className="text-sm">© 2024 VERITAS. All news reserved.</p>

        <div className="flex items-center justify-center gap-4 mt-3">
          <a
            className="w-9 h-9 rounded-full border border-slate-200 flex items-center justify-center text-slate-500 hover:bg-slate-50"
            href="#"
          >
            <i className="fa-brands fa-twitter"></i>
          </a>
          <a
            className="w-9 h-9 rounded-full border border-slate-200 flex items-center justify-center text-slate-500 hover:bg-slate-50"
            href="#"
          >
            <i className="fa-brands fa-facebook-f"></i>
          </a>
          <a
            className="w-9 h-9 rounded-full border border-slate-200 flex items-center justify-center text-slate-500 hover:bg-slate-50"
            href="#"
          >
            <i className="fa-brands fa-linkedin-in"></i>
          </a>
        </div>
      </div>
    </footer>
  );
}
