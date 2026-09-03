# -*- coding: utf-8 -*-
"""音效引擎重做：FM钟琴+卷积混响+滤波噪声+境界氛围垫底+主音量"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

start = c.find("//#region audio")
end = c.find("//#endregion", start)
assert start != -1 and end != -1, "audio region not found"
new_region = """//#region audio — 重做：FM钟琴 + 卷积混响 + 滤波噪声扫频 + 境界氛围垫底
		let actx, masterGain, reverb, ambNodes = [];
		const ac = () => {
			if (!actx) {
				try {
					actx = new (window.AudioContext || window.webkitAudioContext)();
					masterGain = actx.createGain();
					masterGain.gain.value = (parseFloat(localStorage.getItem("nitian.vol") || "0.6"));
					masterGain.connect(actx.destination);
					// 卷积混响：合成小厅堂脉冲
					reverb = actx.createConvolver();
					reverb.buffer = makeIR(actx, 1.8, 2.4);
					const rg = actx.createGain(); rg.gain.value = 0.32;
					reverb.connect(rg); rg.connect(masterGain);
				} catch { }
			}
			return actx;
		};
		function makeIR(ctx, seconds, decay) {
			const len = Math.floor(ctx.sampleRate * seconds);
			const buf = ctx.createBuffer(2, len, ctx.sampleRate);
			for (let ch = 0; ch < 2; ch++) {
				const d = buf.getChannelData(ch);
				for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, decay);
			}
			return buf;
		}
		function bell(ctx, freq, dur, vol, detunePartial) {
			// FM 钟琴：载波 + 非谐波泛音，指数衰减进混响
			const t = ctx.currentTime;
			const out = ctx.createGain();
			out.gain.value = 0;
			out.gain.setValueAtTime(0, t);
			out.gain.linearRampToValueAtTime(vol, t + 0.01);
			out.gain.exponentialRampToValueAtTime(0.0001, t + dur);
			out.connect(masterGain);
			out.connect(reverb);
			const mod = ctx.createOscillator(); mod.frequency.value = freq * 1.0;
			const mg = ctx.createGain(); mg.gain.value = freq * 0.5;
			mod.connect(mg); mg.connect(out);
			const partials = [1, 2.42, 3.7, 5.3, detunePartial || 7.1];
			partials.forEach((ratio, k) => {
				const o = ctx.createOscillator(); o.type = "sine"; o.frequency.value = freq * ratio;
				const g = ctx.createGain(); g.gain.value = vol * (0.5 / (k + 1));
				g.gain.setValueAtTime(g.gain.value, t);
				g.gain.exponentialRampToValueAtTime(0.0001, t + dur * (1 - k * 0.08));
				o.connect(g); g.connect(out);
				o.start(t); o.stop(t + dur + 0.05);
			});
			mod.start(t); mod.stop(t + dur + 0.05);
		}
		function whoosh(ctx, up, dur, vol) {
			// 滤波噪声扫频
			const t = ctx.currentTime;
			const buf = ctx.createBuffer(1, ctx.sampleRate * dur, ctx.sampleRate);
			const d = buf.getChannelData(0);
			for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
			const src = ctx.createBufferSource(); src.buffer = buf;
			const f = ctx.createBiquadFilter(); f.type = "bandpass"; f.Q.value = 1.6;
			f.frequency.setValueAtTime(up ? 300 : 1400, t);
			f.frequency.exponentialRampToValueAtTime(up ? 2600 : 240, t + dur);
			const g = ctx.createGain(); g.gain.setValueAtTime(0.0001, t);
			g.gain.exponentialRampToValueAtTime(vol, t + dur * 0.3);
			g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
			src.connect(f); f.connect(g); g.connect(masterGain);
			src.start(t); src.stop(t + dur);
		}
		function sfxGong() { const c = ac(); if (!c) return; bell(c, 118, 3.6, 0.5, 4.3); bell(c, 186.5, 2.8, 0.28, 5.1); setTimeout(() => bell(c, 233, 2.4, 0.18, 6.2), 140); }
		function sfxRise() { const c = ac(); if (!c) return; whoosh(c, true, 1.2, 0.5); bell(c, 660, 2.6, 0.22, 6.0); }
		function sfxDoom() { const c = ac(); if (!c) return; const t = c.currentTime;
			const o = c.createOscillator(), o2 = c.createOscillator(), g = c.createGain();
			o.type = "sawtooth"; o.frequency.setValueAtTime(82, t); o.frequency.linearRampToValueAtTime(46, t + 1.1);
			o2.type = "sawtooth"; o2.frequency.setValueAtTime(82.7, t); o2.frequency.linearRampToValueAtTime(46.3, t + 1.1);
			g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.12, t + 0.15);
			g.gain.exponentialRampToValueAtTime(0.0001, t + 1.3);
			const lf = c.createBiquadFilter(); lf.type = "lowpass"; lf.frequency.value = 320;
			o.connect(lf); o2.connect(lf); lf.connect(g); g.connect(masterGain);
			o.start(t); o2.start(t); o.stop(t + 1.4); o2.stop(t + 1.4);
			bell(c, 55, 1.6, 0.22, 3.1); whoosh(c, false, 0.8, 0.25);
		}
		function setVolume(v) { try { if (masterGain) masterGain.gain.value = v; localStorage.setItem("nitian.vol", String(v)); } catch { } }
		// 境界氛围垫底：两失谐振荡器 + 慢 LFO，随境界色/调变化
		function setAmbient(n) {
			const c = ac(); if (!c) return;
			ambNodes.forEach(n2 => { try { n2.stop(); } catch { } });
			ambNodes = [];
			if (!n) return;
			const f0 = 55 + (n % 12) * 2.5;
			[1, 1.003].forEach((r, k) => {
				const o = c.createOscillator(); o.type = "sine"; o.frequency.value = f0 * r;
				const g = c.createGain(); g.gain.value = 0.018;
				const lfo = c.createOscillator(); lfo.frequency.value = 0.06 + k * 0.03;
				const lg = c.createGain(); lg.gain.value = 0.008;
				lfo.connect(lg); lg.connect(g.gain);
				o.connect(g); g.connect(masterGain);
				o.start(); lfo.start();
				ambNodes.push(o, lfo);
			});
		}
		//#endregion"""
c = c[:start] + new_region + c[end + len("//#endregion"):]
f.write_text(c, encoding="utf-8")
print("audio engine rebuilt")