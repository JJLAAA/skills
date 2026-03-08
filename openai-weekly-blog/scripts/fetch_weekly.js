const https = require('https');

// 获取本周范围：从最近的周日到周六
const now = new Date();
const dayOfWeek = now.getDay();

// 如果今天是周日到周六，找到本周的周日
let weekStart = new Date(now);
weekStart.setDate(now.getDate() - dayOfWeek);
weekStart.setHours(0, 0, 0, 0);

// 本周六
let weekEnd = new Date(weekStart);
weekEnd.setDate(weekStart.getDate() + 6);
weekEnd.setHours(23, 59, 59, 999);

// 如果今天是周日之后，且周还没结束，使用上一周
if (dayOfWeek > 0 && now < weekEnd) {
  // 当前周还在进行中，使用上一周的完整周
  weekStart.setDate(weekStart.getDate() - 7);
  weekEnd.setDate(weekEnd.getDate() - 7);
}

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
