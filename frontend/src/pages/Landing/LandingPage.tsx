import React from 'react';
import { Hero } from './components/Hero';
import { Features } from './components/Features';
import { Pricing } from './components/Pricing';
import { Testimonials } from './components/Testimonials';
import { Contact } from './components/Contact';

export const LandingPage: React.FC = () => (
  <div className="bg-white">
    <Hero />
    <Features />
    <Pricing />
    <Testimonials />
    <Contact />
  </div>
);

export default LandingPage;
