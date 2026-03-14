/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { Box, Text } from 'ink';
import { UserIdentity } from './UserIdentity.js';
import { Tips } from './Tips.js';
import { useSettings } from '../contexts/SettingsContext.js';
import { useConfig } from '../contexts/ConfigContext.js';
import { useUIState } from '../contexts/UIStateContext.js';
import { Banner } from './Banner.js';
import { useBanner } from '../hooks/useBanner.js';
import { useTips } from '../hooks/useTips.js';
import { theme } from '../semantic-colors.js';
import { ThemedGradient } from './ThemedGradient.js';
import { CliSpinner } from './CliSpinner.js';
import {
  shortAsciiLogo,
  longAsciiLogo,
  tinyAsciiLogo,
  shortAsciiLogoBaseWidth,
  longAsciiLogoBaseWidth,
  tinyAsciiLogoBaseWidth,
} from './AsciiArt.js';
import { getAsciiArtWidth } from '../utils/textUtils.js';
import { useSnowfall } from '../hooks/useSnowfall.js';

import { isAppleTerminal } from '@google/gemini-cli-core';

interface AppHeaderProps {
  version: string;
  showDetails?: boolean;
}

const DEFAULT_ICON = `▝▜▄  
  ▝▜▄
 ▗▟▀ 
▝▀    `;

/**
 * The default Apple Terminal.app adds significant line-height padding between
 * rows. This breaks Unicode block-drawing characters that rely on vertical
 * adjacency (like half-blocks). This version is perfectly symmetric vertically,
 * which makes the padding gaps look like an intentional "scanline" design
 * rather than a broken image.
 */
const MAC_TERMINAL_ICON = `▝▜▄  
  ▝▜▄
  ▗▟▀
▗▟▀  `;

export const AppHeader = ({ version, showDetails = true }: AppHeaderProps) => {
  const settings = useSettings();
  const config = useConfig();
  const { terminalWidth, bannerData, bannerVisible, updateInfo } = useUIState();

  const { bannerText } = useBanner(bannerData);
  const { showTips } = useTips();

  const showHeader = !(
    settings.merged.ui.hideBanner || config.getScreenReader()
  );

  const ICON = isAppleTerminal() ? MAC_TERMINAL_ICON : DEFAULT_ICON;

  const widthOfLongLogo = getAsciiArtWidth(longAsciiLogo);
  const widthOfShortLogo = getAsciiArtWidth(shortAsciiLogo);
  let displayLogo;
  let logoBaseWidth: number;
  if (terminalWidth >= widthOfLongLogo) {
    displayLogo = longAsciiLogo;
    logoBaseWidth = longAsciiLogoBaseWidth;
  } else if (terminalWidth >= widthOfShortLogo) {
    displayLogo = shortAsciiLogo;
    logoBaseWidth = shortAsciiLogoBaseWidth;
  } else {
    displayLogo = tinyAsciiLogo;
    logoBaseWidth = tinyAsciiLogoBaseWidth;
  }
  const logoWidth = getAsciiArtWidth(displayLogo);
  const animatedLogo = useSnowfall(displayLogo);

  if (!showDetails) {
    return (
      <Box flexDirection="column">
        {showHeader && (
          <Box
            flexDirection="row"
            marginTop={1}
            marginBottom={1}
            paddingLeft={2}
          >
            <Box flexShrink={0}>
              <ThemedGradient>{ICON}</ThemedGradient>
            </Box>
            <Box marginLeft={2} flexDirection="column">
              <Box>
                <Text bold color={theme.text.primary}>
                  GeminiZ
                </Text>
                <Text color={theme.text.secondary}> v{version}</Text>
              </Box>
            </Box>
          </Box>
        )}
      </Box>
    );
  }

  return (
    <Box flexDirection="column">
      {showHeader && (
        <Box
          marginTop={1}
          alignItems="flex-start"
          width={logoWidth}
          flexShrink={0}
          flexDirection="column"
        >
          {animatedLogo
            .split('\n')
            .filter(Boolean)
            .map((line, i) => (
              <Box key={i} flexDirection="row">
                <ThemedGradient>{line.slice(0, logoBaseWidth)}</ThemedGradient>
                {line.length > logoBaseWidth && (
                  <Text color="#00e676">{line.slice(logoBaseWidth)}</Text>
                )}
              </Box>
            ))}
        </Box>
      )}
      {showHeader && (
        <Box flexDirection="row" marginBottom={1} paddingLeft={2}>
          <Box flexShrink={0}>
            <ThemedGradient>{ICON}</ThemedGradient>
          </Box>
          <Box marginLeft={2} flexDirection="column">
            {/* Line 1: GeminiZ vVersion [Updating] */}
            <Box>
              <Text bold color={theme.text.primary}>
                GeminiZ
              </Text>
              <Text color={theme.text.secondary}> v{version}</Text>
              {updateInfo && (
                <Box marginLeft={2}>
                  <Text color={theme.text.secondary}>
                    <CliSpinner /> Updating
                  </Text>
                </Box>
              )}
            </Box>

            {/* Line 2: Blank */}
            <Box height={1} />

            {/* Lines 3 & 4: User Identity info (Email /auth and Plan /upgrade) */}
            {settings.merged.ui.showUserIdentity !== false && (
              <UserIdentity config={config} />
            )}
          </Box>
        </Box>
      )}

      {bannerVisible && bannerText && (
        <Banner
          width={terminalWidth}
          bannerText={bannerText}
          isWarning={bannerData.warningText !== ''}
        />
      )}

      {!(settings.merged.ui.hideTips || config.getScreenReader()) &&
        showTips && <Tips config={config} />}
    </Box>
  );
};
