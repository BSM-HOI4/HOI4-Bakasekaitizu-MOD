/**
 * Settings Store - Application settings including language
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Language, getTranslations, I18nStrings } from '../i18n';

interface SettingsState {
  language: Language;
  t: I18nStrings;
  
  setLanguage: (lang: Language) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      language: 'ja', // Default to Japanese
      t: getTranslations('ja'),
      
      setLanguage: (lang: Language) => {
        set({
          language: lang,
          t: getTranslations(lang),
        });
      },
    }),
    {
      name: 'map-ide-settings',
      partialize: (state) => ({ language: state.language }),
      onRehydrateStorage: () => (state) => {
        if (state) {
          state.t = getTranslations(state.language);
        }
      },
    }
  )
);
