# NRL Predictions - User Guide

**If you just want to see the predictions and don't care about the technical stuff, this is for you!**

---

## 🎯 Quick Start

### On Mac or Linux (Terminal):
```bash
python get_predictions.py
```

### On Windows (Command Prompt or PowerShell):
```bash
python get_predictions.py
```

That's it! You'll see all this week's NRL predictions.

---

## 📋 Options

### See a specific round:
```bash
python get_predictions.py --round 5
python get_predictions.py -r 10
```

### See predictions in a beautiful webpage:
```bash
python get_predictions.py --html
```
Then open `predictions_round_X.html` in your browser.

### See Women's NRL (NRLW) predictions:
```bash
python get_predictions.py --competition nrlw
```

### See a different year:
```bash
python get_predictions.py --year 2025
```

---

## 📱 Example Output

```
============================================================
  🏉 NRL PREDICTIONS - Round 5
============================================================

MATCH 1: Panthers vs Storm
--------------------------------------------------
  🏠 Panthers           62% ████████████
  ✈️  Storm             38% ██████
  🎯 Predicted Winner: Panthers
  📊 Confidence: 7.2/10
  📍 Venue: BlueBet Stadium
  🕐 Kickoff: Saturday, 7:35 PM

...
============================================================
  Generated: 2026-02-12 09:00
============================================================
```

---

## 💡 Tips

1. **Higher confidence = More sure the prediction is correct**
   - 8-10/10: Very confident
   - 5-7/10: Moderate
   - 1-4/10: Toss-up game

2. **Check the HTML version for a prettier view**
   - Colors make it easier to read
   - Mobile-friendly design

3. **Predictions update automatically**
   - Just run the script again anytime
   - Uses the latest team data

---

## ❓ Troubleshooting

**"python: command not found"**
- On Mac: Install Python from https://python.org
- On Windows: Install Python and check "Add to PATH"

**"No matches found"**
- The fixtures might not be released yet
- Try a different round number

**"Module not found" errors**
- Run from the project directory:
  ```bash
  cd /path/to/nrl-predictions
  python get_predictions.py
  ```

---

## 📞 Need Help?

- Open an issue on GitHub: https://github.com/sylvery/NRL-predictions/issues
- Check the main README for more details

---

**Enjoy the predictions! 🏉**
