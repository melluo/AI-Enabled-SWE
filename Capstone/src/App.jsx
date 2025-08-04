import React, { useState, useMemo } from 'react';
import { HeartIcon, ArrowPathIcon } from '@heroicons/react/24/solid';

/**
 * @typedef {Object} AffirmationCardProps
 * @property {string[]} affirmations - An array of affirmation strings to display.
 * @property {string} [initialAffirmation] - The first affirmation to show. Defaults to the first item in the array.
 */

/**
 * A UI component that displays an affirmation and allows the user to generate a new one.
 * It's designed to be self-contained, managing its own state for the current affirmation.
 *
 * @param {AffirmationCardProps} props
 */
const AffirmationCard = ({ affirmations, initialAffirmation }) => {
  // Memoize the initial affirmation to prevent re-renders from changing it if the prop reference changes.
  const firstAffirmation = useMemo(() => {
    return initialAffirmation || (affirmations && affirmations.length > 0 ? affirmations[0] : 'You are doing great!');
  }, [affirmations, initialAffirmation]);
  
  // State for the currently displayed affirmation.
  const [currentAffirmation, setCurrentAffirmation] = useState(firstAffirmation);

  // Handler to get a new random affirmation from the list.
  // It ensures the new affirmation is different from the current one if possible.
  const handleNewAffirmation = () => {
    if (!affirmations || affirmations.length === 0) return;

    let newIndex;
    let newAffirmation;

    do {
      newIndex = Math.floor(Math.random() * affirmations.length);
      newAffirmation = affirmations[newIndex];
    } while (affirmations.length > 1 && newAffirmation === currentAffirmation);
    
    setCurrentAffirmation(newAffirmation);
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 pt-10 max-w-md w-full text-center flex flex-col items-center space-y-6 transform transition-all duration-300 hover:shadow-2xl">
      {/* Top Icon */}
      <div className="text-red-500">
        <HeartIcon className="h-16 w-16" />
      </div>

      {/* Category Title */}
      <h2 className="text-sm font-medium text-gray-500 uppercase tracking-widest">
        Affirmation
      </h2>

      {/* Main Affirmation Text */}
      <p className="text-3xl font-bold text-gray-800 leading-snug">
        "{currentAffirmation}"
      </p>

      {/* Call-to-Action Button */}
      <button
        onClick={handleNewAffirmation}
        className="
          flex items-center justify-center space-x-2 px-6 py-3 mt-4
          font-semibold text-white rounded-full
          bg-gradient-to-r from-purple-500 to-pink-500
          shadow-md hover:shadow-lg focus:outline-none 
          focus:ring-2 focus:ring-offset-2 focus:ring-purple-500
          transform hover:-translate-y-1 transition-all duration-200"
      >
        <ArrowPathIcon className="h-5 w-5" />
        <span>New Affirmation</span>
      </button>
    </div>
  );
};

/**
 * This is a wrapper component to demonstrate how to use the AffirmationCard.
 * In a real application, you would import AffirmationCard and use it in your pages.
 */
export default function AffirmationPage() {
  // Sample data. In a real app, this might come from an API.
  const affirmationList = [
    "You are capable of amazing things.",
    "Your potential is limitless.",
    "You are growing stronger every day.",
    "You radiate positivity and joy.",
    "You are worthy of all the good things in life.",
    "You have the power to create the life you desire.",
    "Believe in yourself and all that you are."
  ];

  return (
    // This outer div provides the centered layout and background color shown in the image.
    <div className="bg-slate-100 flex items-center justify-center min-h-screen p-4 font-sans">
      <AffirmationCard affirmations={affirmationList} />
    </div>
  );
}