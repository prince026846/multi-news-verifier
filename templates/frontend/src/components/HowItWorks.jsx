export default function HowItWorks() {
  const steps = [
    {
      id: 1,
      title: "Paste or Upload",
      desc: "User pastes news text or uploads an image/video/audio for verification.",
      icon: "📥",
      color: "bg-blue-100 text-blue-600",
    },
    {
      id: 2,
      title: "AI Analysis",
      desc: "The AI model analyzes the content across multiple languages and formats.",
      icon: "🤖",
      color: "bg-green-100 text-green-600",
    },
    {
      id: 3,
      title: "Results",
      desc: "Output shows whether news is Fact, Fake, or Needs Proof, backed by sources.",
      icon: "✅",
      color: "bg-purple-100 text-purple-600",
    },
  ];

  return (
    <section className="bg-gray-50 py-16">
      <div className="max-w-6xl mx-auto px-6">
        {/* Title */}
        <h1 className="text-4xl font-extrabold text-center text-gray-900 mb-6">
          How It Works
        </h1>
        <p className="text-center text-lg text-gray-600 max-w-2xl mx-auto mb-12">
          Verifying news is simple. Follow these quick steps to check if content
          is <span className="font-semibold">real or fake</span>.
        </p>

        {/* Steps */}
        <div className="relative">
          {/* Vertical line for flow */}
          <div className="hidden md:block absolute top-0 left-1/2 transform -translate-x-1/2 h-full border-l-2 border-dashed border-gray-300"></div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className="relative flex flex-col items-center text-center"
              >
                {/* Icon */}
                <div
                  className={`${step.color} w-20 h-20 rounded-full flex items-center justify-center text-3xl font-bold shadow-md mb-4`}
                >
                  {step.icon}
                </div>

                {/* Step number */}
                <span className="text-sm uppercase tracking-wide text-gray-500 mb-2">
                  Step {step.id}
                </span>

                {/* Title */}
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {step.title}
                </h3>

                {/* Description */}
                <p className="text-gray-600">{step.desc}</p>

                {/* Connecting dot */}
                {index !== steps.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 right-[-2.5rem] transform translate-y-[-50%]">
                    <div className="w-5 h-5 rounded-full bg-blue-500 shadow"></div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
