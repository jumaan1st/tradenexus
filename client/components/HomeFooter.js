import Link from "next/link"

export default function HomeFooter() {
    return(
        
      <footer className="bg-[#0B1340] text-[#A5BFFA] p-8">
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div>
            <h4 className="text-white font-semibold mb-4">TRADENEXUS AI</h4>
            <p>AI that Thinks Finance, empowering investors with cutting-edge technology.</p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li><Link href="/about" className="hover:text-white transition">About</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Connect</h4>
            <ul className="space-y-2">
              <li><a href="mailto:support@tradenexus.ai" className="hover:text-white transition">support@tradenexus.ai</a></li>
              <li><Link href="/#" className="hover:text-white transition">Privacy Policy</Link></li>
              <li><Link href="/#features" className="hover:text-white transition">Terms of Service</Link></li>
            </ul>
          </div>
        </div>
        <p className="text-center mt-8">© 2025 TRADENEXUS AI. All rights reserved.</p>
      </footer>
    )
}