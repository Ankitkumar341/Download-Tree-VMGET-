import React, { useState } from 'react';
import { Download, Link as LinkIcon } from 'lucide-react';

interface DownloadCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  supportedFormats: string[];
  onDownload: (url: string, format: string) => void;
  variant: 'youtube' | 'instagram' | 'pinterest';
}

const DownloadCard: React.FC<DownloadCardProps> = ({
  title,
  description,
  icon,
  supportedFormats,
  onDownload,
  variant,
}) => {
  const [url, setUrl] = useState('');
  const [selectedFormat, setSelectedFormat] = useState(supportedFormats[0]);

  const variants = {
    youtube: {
      gradient: 'from-red-500 to-red-700',
      iconColor: 'text-red-600',
      buttonBg: 'bg-red-600 hover:bg-red-700',
      ringColor: 'focus:ring-red-600 focus:border-red-600',
    },
    instagram: {
      gradient: 'from-pink-500 via-purple-500 to-indigo-500',
      iconColor: 'text-pink-600',
      buttonBg: 'bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500 hover:from-pink-600 hover:via-purple-600 hover:to-indigo-600',
      ringColor: 'focus:ring-purple-600 focus:border-purple-600',
    },
    pinterest: {
      gradient: 'from-red-600 to-red-800',
      iconColor: 'text-red-700',
      buttonBg: 'bg-red-700 hover:bg-red-800',
      ringColor: 'focus:ring-red-700 focus:border-red-700',
    },
  };

  const currentVariant = variants[variant];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onDownload(url, selectedFormat);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden transform transition-all hover:scale-105">
      <div className={`h-2 bg-gradient-to-r ${currentVariant.gradient}`} />
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-gray-900">{title}</h3>
          <div className={currentVariant.iconColor}>{icon}</div>
        </div>
        
        <p className="text-gray-600 mb-6">{description}</p>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <LinkIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste URL here"
              className={`block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-2 ${currentVariant.ringColor}`}
              required
            />
          </div>
          
          <select
            value={selectedFormat}
            onChange={(e) => setSelectedFormat(e.target.value)}
            className={`block w-full px-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-2 ${currentVariant.ringColor}`}
          >
            {supportedFormats.map((format) => (
              <option key={format} value={format}>
                {format}
              </option>
            ))}
          </select>
          
          <button
            type="submit"
            className={`w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-white ${currentVariant.buttonBg} focus:outline-none focus:ring-2 focus:ring-offset-2 ${currentVariant.ringColor}`}
          >
            <Download className="h-5 w-5 mr-2" />
            Download
          </button>
        </form>
      </div>
    </div>
  );
};

export default DownloadCard;