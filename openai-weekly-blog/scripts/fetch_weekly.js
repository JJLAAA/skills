const https = require('https');

// 从命令行参数获取日期，格式 YYYYMMDD（如 20260314）
const dateArg = process.argv[2];
if (!dateArg || !/^\d{8}$/.test(dateArg)) {
  console.error(JSON.stringify({ error: '请提供日期参数，格式为 YYYYMMDD，例如：node fetch_weekly.js 20260314' }));
  process.exit(1);
}

// 解析输入日期作为结束日期
const year = parseInt(dateArg.slice(0, 4));
const month = parseInt(dateArg.slice(4, 6)) - 1; // 0-indexed
const day = parseInt(dateArg.slice(6, 8));

let weekEnd = new Date(year, month, day, 23, 59, 59, 999);

// 找到该日期所在周的周日作为开始日期
const dayOfWeek = weekEnd.getDay(); // 0=Sunday, 6=Saturday
let weekStart = new Date(weekEnd);
weekStart.setDate(weekEnd.getDate() - dayOfWeek);
weekStart.setHours(0, 0, 0, 0);

https.get('https://openai.com/news/rss.xml', (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    const itemMatches = data.match(/<item>[\s\S]*?<\/item>/g) || [];
    const articles = [];

    itemMatches.forEach(itemXml => {
      const title = (itemXml.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/) || [])[1];
      const link = (itemXml.match(/<link>(.*?)<\/link>/) || [])[1];
      const pubDate = (itemXml.match(/<pubDate>(.*?)<\/pubDate>/) || [])[1];
      const description = (itemXml.match(/<description><!\[CDATA\[(.*?)\]\]><\/description>/) || [])[1];
      const categoryMatches = [...itemXml.matchAll(/<category><!\[CDATA\[(.*?)\]\]><\/category>/g)];
      const categories = categoryMatches.map(m => m[1]);

      const hasTarget = categories.some(c => c === 'Research' || c === 'Engineering');
      if (!hasTarget) return;

      const pubDateObj = new Date(pubDate);
      if (pubDateObj >= weekStart && pubDateObj <= weekEnd) {
        const cleanDesc = description.replace(/<[^>]*>/g, '').replace(/&[^;]+;/g, '').trim();
        articles.push({ title, link, pubDate, description: cleanDesc, categories: categories.join(', ') });
      }
    });

    console.log(JSON.stringify({
      articles,
      weekStart: weekStart.toISOString().split('T')[0],
      weekEnd: weekEnd.toISOString().split('T')[0]
    }));
  });
}).on('error', (e) => {
  console.error(JSON.stringify({ error: e.message }));
  process.exit(1);
});
