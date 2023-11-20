import { test, expect } from '@playwright/test';

// Series URL to scrape
const seriesUrl = 'https://areena.yle.fi/1-50552097';

test('Create list of YLE Areena download URLs', async ({ page }) => {
  test.slow();
  await page.goto(seriesUrl);
  await page.waitForTimeout(5000);
  const numberOfSeasons = await page.evaluate(async () => {
    return Array.from(document.querySelectorAll('ol.DesktopDropdown_list__lbvm1 li')).length;
  });
  console.log('Number of seasons:', numberOfSeasons);

  for (let i = 1; i <= numberOfSeasons; i++) {
    await page.getByRole('button', { name: `Kausi ${i}`, exact: true }).click();
    await page.waitForTimeout(1000);
    console.log(`Season ${i} opened`);

    // Extract episode URLs from the website for single season
    let episodeUrls = await page.evaluate(async () => {
      // Replace this selector with the one identifying your list
      const episodes = Array.from(document.querySelectorAll('ul.VerticalList_list__IuYYX li'));
      console.log('Episodes count:', episodes.length);

      return episodes.map((e) => {
        const metaUrl = e.querySelector('meta[itemprop="url"]');
        const url = metaUrl ? metaUrl.getAttribute('content') : null;
        return url;
      });
    });
    
    await page.waitForTimeout(1000);
    
    // Write URLs to file
    const fs = require('fs');
    // Add newline characters between URLs
    let episodeUrlsWithNewline = episodeUrls.join('\n') + '\n';
    await fs.promises.appendFile('urls.txt', episodeUrlsWithNewline, (err) => {
      if (err) throw err
    })
  }
});