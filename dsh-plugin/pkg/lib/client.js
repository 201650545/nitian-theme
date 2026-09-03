window.__ModuleLoader__.load({
	id: "nitian-dsh-theme",
	factory: (require) => {
		var module = { exports: {} };
		var exports = module.exports;
		Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });

		//#region nitian engine v2.1 — 素材全验证版：真官方海报 + U1.5 时代立绘/背景
		const A = "/nitian-assets";
		const P = A + "/officials/posters_season_general";
		const C = A + "/ui/chars";
		const B = A + "/ui/bgs";

		/* 已人工目检为真·官方的图 */
		const V = {
			movie1: P + "/poster_season_movie1_01.jpg",   // 神临之战·红发古神王林（竖）
			movie2: P + "/poster_season_movie2_01.jpg",   // 弑战·银甲黑发王林（竖）
			nianfan2: P + "/poster_season_nianfan2_01.jpg", // 年番·白发红袍+古神之眼（竖）
			nianfan3: P + "/poster_season_nianfan3_01.jpg", // 水墨黑白王林（竖）
			sword: P + "/poster_season_all_01.jpg",       // 定档·巨剑落城（竖）
			yuanyingCG: A + "/collected/yuanying/bg-01.jpg" // 官方CG·王林与李慕婉（横）
		};

		/* U1.5 时代立绘（已裁水印） */
		const CH = {
			ningshi: C + "/era_01_ningshi.png",
			zhuji: C + "/era_02_zhuji.png",
			jiedan: C + "/era_03_jiedan.png",
			yuanying: C + "/era_04_yuanying.png",
			huashen: C + "/era_05_huashen.png",
			yingbian: C + "/era_06_yingbian.png",
			wending: C + "/era_07_wending.png",
			yinyang: C + "/era_08_yinyang.png",
			kong: C + "/era_12_kongnie.png",
			tatian: C + "/era_16_tatian.png"
		};

		/* 背景（横 2048×1152 或官方CG） */
		const BG = {
			ningshi: A + "/realms/01_ningshi/bg.webp",
			zhuji: A + "/realms/02_zhuji/raw/ai_bg_master.png",
			jiedan: A + "/realms/03_jiedan/raw/ai_bg_master.png",
			yuanying: V.yuanyingCG,
			huashen: A + "/realms/05_huashen/raw2/ai_bg_master.png",
			kong: B + "/bg_kongjing.png",
			tatian: B + "/bg_tatian.png"
		};

		const R = (id, name, sub, from, to, main, accent, cur, char, bg, seal, enemy) =>
			({ id, name, sub, from, to, main, accent, cur, char, bg, seal, enemy });

		const REALMS = [
			R("01_ningshi", "凝气期", "恒岳杂役 · 初心起步", 0, 10000, "#c9a55c", "#5a9e8f", "仙玉", CH.ningshi, BG.ningshi, A + "/ui/seals/seal_01_ningshi.png", null),
			R("02_zhuji", "筑基期", "铁柱峰上 · 步步登天", 10000, 100000, "#7fa88f", "#a8c8b0", "仙玉", CH.zhuji, BG.zhuji, A + "/ui/seals/seal_02_zhuji.png", null),
			R("03_jiedan", "结丹期", "灵液化丹 · 杀伐初显", 100000, 1000000, "#b8453a", "#d98a6a", "仙玉", CH.jiedan, BG.jiedan, A + "/ui/seals/seal_03_jiedan.png", V.yuanyingCG),
			R("04_yuanying", "元婴期", "罗天星域 · 纵横一方", 1000000, 10000000, "#3b7fd4", "#7fb2e8", "仙玉", CH.yuanying, BG.yuanying, A + "/ui/seals/seal_04_yuanying.png", null),
			R("05_huashen", "化神期", "神游太虚 · 生死意境", 10000000, 100000000, "#8a9bb5", "#b8c6da", "仙玉", CH.huashen, BG.huashen, A + "/ui/seals/seal_05_huashen.png", null),
			R("06_yingbian", "婴变期", "蜕变之始", 100000000, 1000000000, "#9a6fb8", "#c3a3dd", "仙玉", CH.yingbian, BG.kong, A + "/ui/seals/seal_06_yingbian.png", null),
			R("07_wending", "问鼎期", "问鼎巅峰", 1000000000, 5000000000, "#d0a83c", "#e6cd8a", "仙玉", CH.wending, BG.jiedan, A + "/ui/seals/seal_07_wending.png", null),
			R("08_yinyang", "阴虚阳实", "阴阳跃迁", 5000000000, 20000000000, "#5a9e8f", "#8fc4b8", "仙玉", CH.yinyang, BG.huashen, A + "/ui/seals/seal_08_yinyang.png", null),
			R("09_kunie", "窥涅境", "初窥本源", 20000000000, 100000000000, "#6a89b8", "#a3bcd8", "仙玉", CH.kong, BG.kong, A + "/ui/seals/seal_09_kunie.png", null),
			R("10_jingnie", "净涅境", "涅槃洗尘", 100000000000, 1000000000000, "#4f9bb0", "#93c4d0", "仙玉", CH.yuanying, BG.zhuji, A + "/ui/seals/seal_10_jingnie.png", null),
			R("11_suinie", "碎涅境", "碎涅证道", 1000000000000, 4000000000000, "#b8763a", "#d8a86f", "仙玉", CH.wending, BG.jiedan, A + "/ui/seals/seal_11_suinie.png", null),
			R("12_kongnie", "空涅境", "空之四境 · 其一", 4000000000000, 20000000000000, "#7d6ab8", "#ab9cd8", "香火", CH.kong, BG.kong, A + "/ui/seals/seal_12_kongnie.png", null),
			R("13_kongling", "空灵境", "空之四境 · 其二", 20000000000000, 60000000000000, "#8a7fc9", "#b7abe0", "香火", CH.yuanying, BG.huashen, A + "/ui/seals/seal_13_kongling.png", null),
			R("14_kongxuan", "空玄境", "空之四境 · 其三", 60000000000000, 300000000000000, "#6f89c9", "#a5bbe0", "香火", CH.yingbian, BG.kong, A + "/ui/seals/seal_14_kongxuan.png", null),
			R("15_kongjin", "空劫·金尊", "空劫初境 · 金尊", 300000000000000, 450000000000000, "#c9b45a", "#e2d494", "香火", CH.kong, BG.kong, A + "/ui/seals/seal_15_kongjie.png", null),
			R("16_kongzun", "空劫·天尊", "空劫中境 · 天尊", 450000000000000, 650000000000000, "#d2bd5e", "#e6d494", "香火", CH.kong, BG.kong, A + "/ui/seals/seal_15_kongjie.png", null),
			R("17_kongyue", "空劫·跃天尊", "空劫高境 · 跃天尊", 650000000000000, 850000000000000, "#dcc96a", "#efde9a", "香火", CH.kong, BG.kong, A + "/ui/seals/seal_15_kongjie.png", null),
			R("18_kongda", "空劫·大天尊", "空劫圆满 · 大天尊", 850000000000000, 1000000000000000, "#e6d574", "#f8eaAe", "香火", CH.kong, BG.kong, A + "/ui/seals/seal_15_kongjie.png", null),
			R("19_qiao1", "踏天一桥", "初登天桥", 1000000000000000, 3000000000000000, "#e0c05a", "#f0dc9a", "愿力", CH.tatian, BG.tatian, null, null),
			R("20_qiao2", "踏天二桥", "步步生莲", 3000000000000000, 1e+16, "#dcb84f", "#f0dc9a", "愿力", CH.tatian, BG.tatian, null, null),
			R("21_qiao3", "踏天三桥", "风起云涌", 1e+16, 3e+16, "#d8b045", "#f0dc9a", "愿力", CH.tatian, BG.tatian, null, null),
			R("22_qiao4", "踏天四桥", "俯瞰众生", 3e+16, 1e+17, "#d4a83b", "#eed488", "愿力", CH.tatian, BG.tatian, null, null),
			R("23_qiao5", "踏天五桥", "半渡之境", 1e+17, 3e+17, "#d0a031", "#ecd078", "愿力", CH.tatian, BG.tatian, null, null),
			R("24_qiao6", "踏天六桥", "桥心悟道", 3e+17, 1e+18, "#cc9828", "#e8ca6c", "愿力", CH.tatian, BG.tatian, null, null),
			R("25_qiao7", "踏天七桥", "天涯咫尺", 1e+18, 3e+18, "#c89020", "#e4c460", "愿力", CH.tatian, BG.tatian, null, null),
			R("26_qiao8", "踏天八桥", "唯我独尊", 3e+18, 1e+19, "#c48818", "#e0be54", "愿力", CH.tatian, BG.tatian, null, null),
			R("27_qiao9", "踏天九桥", "彼岸在望 · 大道尽头", 1e19, Infinity, "#ffd700", "#fff3b0", "愿力", CH.tatian, BG.tatian, null, null)
		];

		const QUOTES = {
			"01_ningshi": "顺为凡，逆则仙，只在心中一念间。",
			"03_jiedan": "杀伐果断，方证道途。",
			"04_yuanying": "罗天星域，谁主沉浮。",
			"05_huashen": "神游太虚，生死一念。",
			"08_yinyang": "阴阳逆转，我命由我。",
			"15_kongjie": "金尊天尊，不过途中一阶。",
			default: "道阻且长，行则将至。"
		};
		const SPLASH_LINE = "顺为凡　逆则仙　只在心中一念间";

		const RELABEL = [
			[/^新会话$/, "新开洞府"], [/^新对话$/, "新开洞府"], [/^new chat$/i, "新开洞府"], [/^new session$/i, "新开洞府"],
			[/^工作区$/, "洞府"], [/^sessions?$/i, "洞府"], [/^history$/i, "洞府录"], [/^chats?$/i, "洞府"],
			[/^设置$/, "道藏"], [/^settings$/i, "道藏"],
			[/^描述你想要构建的内容$/, "入定论道 · 述说你的道途"], [/^describe what to build/i, "入定论道 · 述说你的道途"],
			[/^full access$/i, "全权"], [/^fast$/i, "疾速"], [/^balanced$/i, "守衡"],
			[/^send$/i, "传讯"], [/^stop$/i, "收势"],
			[/^terminal$/i, "炼器房"], [/^files?$/i, "器库"], [/^plan(s)?$/i, "推演"], [/^goals?$/i, "心愿"],
			[/^DSH Local Build$/i, "逆天修行录"],
			[/^skills$/i, "神通"], [/^usage$/i, "功德簿"], [/^feedback$/i, "传音"]
		];

		const LS = { demo: "nitian.demoTokens", opt: "nitian.opts.v2", seen: "nitian.splashSeen" };
		const fmt = (n) => n >= 1e15 ? (n / 1e15).toFixed(2) + "P" : n >= 1e12 ? (n / 1e12).toFixed(2) + "T" : n >= 1e9 ? (n / 1e9).toFixed(2) + "B" : n >= 1e6 ? (n / 1e6).toFixed(2) + "M" : n >= 1e3 ? (n / 1e3).toFixed(1) + "K" : String(Math.floor(n));
		const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
		const hexA = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`; };

		function loadOpts() { try { return Object.assign({ audio: true, companion: true, relabel: true, skin: true, ambient: true }, JSON.parse(localStorage.getItem(LS.opt) || "{}")); } catch { return { audio: true, companion: true, relabel: true, skin: true }; } }
		function saveOpts(o) { localStorage.setItem(LS.opt, JSON.stringify(o)); }
		function demoTokens() { return parseFloat(localStorage.getItem(LS.demo) || "0"); }
		function realmOf(t) { for (let k = REALMS.length - 1; k >= 0; k--) if (t >= REALMS[k].from) return k; return 0; }

		//#region audio — 重做：FM钟琴 + 卷积混响 + 滤波噪声扫频 + 境界氛围垫底
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
		//#endregion

		//#region page-level skin css
		const PAGE_CSS = `
html,body{background:#06080c !important}
#root{position:relative;z-index:2;background:transparent !important}
#root>div:first-child{background:transparent !important}
/* 官方吉祥物/装饰/hero 全下架 */
svg[class*="_fish"],img[class*="_fish"],svg[class*="_heroGlow"],div[class*="_heroGlow"],
div[class*="_composerHero"],div[class*="_previewBadge"]{display:none !important}
/* 三栏透明化 */
div[class$="_frame"]{background:transparent !important}
div[class*="_sidebarCol"],div[class*="_detailsCol"]{background:linear-gradient(180deg,rgba(8,11,17,.86),rgba(8,11,17,.78)) !important;backdrop-filter:blur(18px)}
div[class*="_centerCol"]{background:transparent !important}
div[class*="_centerCol"]>div{background:transparent !important}
div[class*="_scrollBody"],div[class*="_composerStack"],div[class*="_composerSeat"]{background:transparent !important}
div[class*="_centerCol"] div[class*="_root"]{background:transparent !important}
/* 洞府侧栏 · 随境界流动的主题 */
div[class*="_sidebarCol"]{background:linear-gradient(180deg,color-mix(in srgb,var(--nit-m,#c9a55c) 9%,rgba(7,10,16,.94)),rgba(7,10,16,.88) 42%) !important;backdrop-filter:blur(18px)}
div[class*="_sidebarCol"] div[class*="_root"]{position:relative}
div[class*="_sidebarCol"] div[class*="_root"]::before{content:"";position:absolute;top:0;bottom:0;right:0;width:2px;background:linear-gradient(180deg,transparent,var(--nit-m,#c9a55c),transparent);opacity:.55;pointer-events:none;z-index:6}
button[class*="_brand"]{color:var(--nit-m,#c9a55c) !important;letter-spacing:.14em;font-weight:700;text-shadow:0 0 14px color-mix(in srgb,var(--nit-m) 55%,transparent)}
button[class*="_brand"] svg{display:none}
button[class*="_brand"]::before{content:"";display:inline-block;width:20px;height:20px;margin-right:8px;background:var(--nit-seal) center/contain no-repeat;vertical-align:-4px;filter:drop-shadow(0 0 6px color-mix(in srgb,var(--nit-m) 60%,transparent))}
button[class*="_newSession"]{background:linear-gradient(135deg,color-mix(in srgb,var(--nit-m) 24%,transparent),color-mix(in srgb,var(--nit-a) 16%,transparent)) !important;border:1px solid color-mix(in srgb,var(--nit-m) 45%,transparent) !important;color:#e6ddc8 !important;border-radius:12px !important}
button[class*="_newSession"]:hover{border-color:var(--nit-m) !important;box-shadow:0 0 18px color-mix(in srgb,var(--nit-m) 35%,transparent)}
`;
		//#endregion

		function apply(ctx) {
			if (window.__NITIAN_BOOTED__) return;
			window.__NITIAN_BOOTED__ = true;

			const opts = loadOpts();
			let idx = -1;
			let realTokens = 0;
			let lastErrorAt = 0;

			if (opts.skin) {
				const pageStyle = document.createElement("style");
				pageStyle.id = "nitian-page-css";
				pageStyle.textContent = PAGE_CSS;
				document.head.appendChild(pageStyle);
			}

			/* 背景层 */
			const bgHost = document.createElement("div");
			bgHost.id = "nitian-bglayer";
			bgHost.style.cssText = "position:fixed;inset:0;z-index:0;pointer-events:none";
			bgHost.innerHTML = `<img id="nb-a" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1.6s ease"><img id="nb-b" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1.6s ease"><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,7,11,.66),rgba(5,7,11,.52) 42%,rgba(5,7,11,.8))"></div><div class="nv" style="position:absolute;inset:0;transition:background 1.4s ease"></div>`;
			const rootEl = document.getElementById("root") || document.body;
			rootEl.parentNode.insertBefore(bgHost, rootEl);
			const bgImgs = [bgHost.querySelector("#nb-a"), bgHost.querySelector("#nb-b")];
			let bgSlot = 0;
			function setBg(url) {
				if (!url) return;
				const next = bgImgs[bgSlot ^ 1], cur = bgImgs[bgSlot];
				if ((next.dataset.src || "") === url) return;
				next.dataset.src = url;
				next.onload = () => { next.style.opacity = "1"; cur.style.opacity = "0"; bgSlot ^= 1; };
				next.src = url;
			}

			/* UI 主层 */
			const host = document.createElement("div");
			host.id = "nitian-host";
			document.documentElement.appendChild(host);
			const shadow = host.attachShadow({ mode: "open" });
			const style = document.createElement("style");
			style.textContent = `
:host{all:initial;font-family:"Microsoft YaHei","PingFang SC",system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
.nr{position:fixed;inset:0;pointer-events:none;z-index:2147400000}
.hud{position:absolute;top:12px;left:50%;transform:translateX(-50%);pointer-events:auto;display:flex;align-items:center;gap:12px;padding:8px 18px;border-radius:999px;background:linear-gradient(135deg,rgba(9,12,18,.94),rgba(16,22,34,.94));border:1px solid color-mix(in srgb,var(--m) 55%,transparent);box-shadow:0 4px 26px rgba(0,0,0,.5);backdrop-filter:blur(8px)}
.hud .seal{width:34px;height:34px;border-radius:50%;object-fit:cover;border:1.5px solid var(--a);background:#0b0e15}
.hud .bridge{width:34px;height:34px;border-radius:50%;border:1.5px solid var(--a);color:var(--m);display:none;align-items:center;justify-content:center;font-size:15px;font-weight:700;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.14),transparent)}
.rt{line-height:1.25}
.rt .rn{color:var(--m);font-weight:700;font-size:14px;letter-spacing:.1em;text-shadow:0 0 10px rgba(255,255,255,.12);white-space:nowrap}
.rt .rs{color:#96a0b5;font-size:10px;letter-spacing:.06em;white-space:nowrap}
.bar{position:relative;width:220px;height:10px;border-radius:6px;background:#111725;overflow:hidden;border:1px solid #2a3348}
.bar>i{position:absolute;inset:0;width:0%;border-radius:6px;background:linear-gradient(90deg,color-mix(in srgb,var(--m) 60%,#000),var(--m));transition:width .9s cubic-bezier(.2,.8,.2,1)}
.bar>b{position:absolute;right:7px;top:-1px;font-size:8.5px;line-height:11px;color:#e6ddc8;font-weight:400;opacity:.9}
.jade{text-align:right;line-height:1.3}
.jade em{font-style:normal;color:#e6ddc8;font-size:12px}.jade em b{color:var(--a)}
.jade span{font-size:9px;color:#8a93a6;display:block}
.track{font-size:9px;color:#7d8698;text-align:right;line-height:1.35}
.track i{font-style:normal;color:#9aa6bd}
.comp{position:absolute;right:18px;bottom:210px;pointer-events:auto;width:150px;border-radius:16px;padding:6px;background:linear-gradient(165deg,rgba(19,25,38,.93),rgba(11,14,21,.95));border:1px solid color-mix(in srgb,var(--m) 50%,transparent);box-shadow:0 10px 34px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.03) inset;cursor:grab;transition:box-shadow .2s;touch-action:none}
.comp:active{cursor:grabbing}
.comp.dragging{opacity:.92;box-shadow:0 14px 44px rgba(0,0,0,.7)}
.comp img{width:100%;aspect-ratio:3/4;object-fit:cover;object-position:center 12%;border-radius:11px;display:block;animation:sway 6s ease-in-out infinite;transform-origin:50% 100%}
@keyframes sway{0%,100%{transform:rotate(-.5deg)}50%{transform:rotate(.5deg)}}
.comp .ground{height:10px;margin:2px 8px 0;border-radius:50%;background:radial-gradient(ellipse at center,color-mix(in srgb,var(--m) 42%,transparent),transparent 68%)}
.comp .cname{margin-top:5px;text-align:center;font-size:11px;color:var(--m);letter-spacing:.3em;text-indent:.3em;padding-bottom:2px}
.comp .csub{text-align:center;font-size:9px;color:#8a93a6;padding-bottom:6px}
.comp .c3d{position:absolute;top:4px;right:28px;width:26px;height:20px;border-radius:9px;border:1px solid #2a3348;background:rgba(11,14,21,.92);color:#8a93a6;font-size:9px;cursor:pointer;z-index:3;padding:0}
.comp .c3d:hover{color:var(--m);border-color:var(--m)}
.comp.mini .c3d{display:none}
.comp .cmin{position:absolute;top:4px;right:4px;width:20px;height:20px;border-radius:50%;border:1px solid #2a3348;background:rgba(11,14,21,.92);color:#8a93a6;font-size:11px;line-height:17px;cursor:pointer;z-index:3;padding:0}
.comp .cmin:hover{color:var(--m);border-color:var(--m)}
.comp.mini{width:58px;padding:3px;border-radius:50%}
.comp.mini img{width:52px;height:52px;aspect-ratio:1/1;border-radius:50%;object-fit:cover;object-position:center 12%;animation:none}
.comp.mini .cname,.comp.mini .csub,.comp.mini .ground{display:none}
.comp.mini .cmin{top:-2px;right:-2px}
.v3d{position:absolute;inset:0;pointer-events:auto;display:none;background:radial-gradient(ellipse at 50% 60%,#101826,#04060a);z-index:6}
.v3d.on{display:block}
.v3d canvas{width:100%;height:100%;display:block}
.v3d .ld{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:#e6ddc8;font-size:13px;letter-spacing:.2em}
.v3d .x{position:absolute;right:24px;top:24px;color:#8a93a6;font-size:12px;letter-spacing:.2em;cursor:pointer;border:1px solid #2a3348;border-radius:999px;padding:7px 24px;pointer-events:auto}
.v3d .x:hover{color:var(--m);border-color:var(--m)}
.v3d .hint{position:absolute;left:50%;bottom:26px;transform:translateX(-50%);color:#79839a;font-size:11px;letter-spacing:.24em}
.insp{position:absolute;inset:0;pointer-events:auto;display:none;align-items:center;justify-content:center;flex-direction:column;gap:18px;background:rgba(4,6,10,.9);backdrop-filter:blur(12px);z-index:5}
.insp.on{display:flex}
.insp img{max-width:min(430px,72vw);max-height:64vh;border-radius:18px;border:1.5px solid var(--m);box-shadow:0 0 80px color-mix(in srgb,var(--m) 38%,transparent);object-fit:cover;object-position:center 10%}
.insp .q{color:#e6ddc8;font-size:16px;letter-spacing:.28em;text-indent:.28em}
.insp .x{margin-top:6px;color:#8a93a6;font-size:11px;letter-spacing:.2em;cursor:pointer;border:1px solid #2a3348;border-radius:999px;padding:6px 22px}
.insp .x:hover{color:var(--m);border-color:var(--m)}
.splash{position:absolute;inset:0;pointer-events:auto;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px;background:rgba(4,6,10,.86);backdrop-filter:blur(12px);transition:opacity .8s;z-index:6}
.splash.off{opacity:0;pointer-events:none}
.splash h1{font-size:32px;color:#efe6cf;letter-spacing:.4em;text-indent:.4em;font-weight:300;text-shadow:0 0 30px color-mix(in srgb,var(--m) 85%,transparent)}
.splash p{font-size:12px;color:#8a93a6;letter-spacing:.24em}
.splash button{padding:11px 46px;font-size:14px;letter-spacing:.5em;text-indent:.5em;color:#0b0e15;background:linear-gradient(135deg,var(--m),var(--a));border:0;border-radius:999px;cursor:pointer;font-weight:700}
.bt{position:absolute;inset:0;pointer-events:auto;display:none;overflow:hidden;background:#04060a;z-index:7}
.bt.on{display:block}
.bt .flash{position:absolute;inset:0;background:radial-gradient(circle at 50% 46%,#fff7dd,#e8c56a 34%,rgba(232,197,106,0) 72%);animation:bf 2.6s ease-out forwards}
@keyframes bf{0%{opacity:0}16%{opacity:.96}44%{opacity:.35}100%{opacity:0}}
.bt .ring{position:absolute;left:50%;top:45%;width:12vmax;height:12vmax;margin:-6vmax;border-radius:50%;border:2px solid #ffe9ad;animation:br 2.4s cubic-bezier(.16,.84,.44,1) forwards;opacity:0}
@keyframes br{0%{transform:scale(.2);opacity:0}18%{opacity:1}100%{transform:scale(9);opacity:0}}
.bt .newseal{position:absolute;left:50%;top:37%;width:158px;height:158px;margin-left:-79px;border-radius:50%;object-fit:cover;border:3px solid var(--m);box-shadow:0 0 70px var(--m);animation:drop 1.5s cubic-bezier(.2,1.4,.4,1) forwards;opacity:0;background:#0b0e15}
.bt .glyph{position:absolute;left:50%;top:37%;width:158px;height:158px;margin-left:-79px;border-radius:50%;border:3px solid var(--m);box-shadow:0 0 70px var(--m);display:none;align-items:center;justify-content:center;font-size:52px;color:var(--m);font-weight:700;background:radial-gradient(circle at 35% 28%,rgba(255,255,255,.12),transparent);animation:drop 1.5s cubic-bezier(.2,1.4,.4,1) forwards;opacity:0}
@keyframes drop{0%{transform:translateY(-46vh) scale(1.7);opacity:0}55%{opacity:1}75%{transform:translateY(0) scale(1)}85%{transform:translateY(-10px)}100%{transform:translateY(0);opacity:1}}
.bt .vid{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:none;background:#04060a}
.bt.playvid .vid{display:block;animation:vfade 1s ease}
.bt.playvid .flash,.bt.playvid .ring,.bt.playvid .shard{display:none}
.bt.playvid .newseal,.bt.playvid .glyph{width:92px;height:92px;margin-left:-46px;left:50%;top:auto;bottom:6%;animation:none;opacity:1;font-size:30px;border-width:2px;box-shadow:0 0 30px var(--m)}
.bt.playvid .verdict{bottom:15%;animation:vfade 1.2s 1.2s both}
.bt.playvid .verdict h2{font-size:26px}
@keyframes vfade{from{opacity:0}to{opacity:1}}
.bt.major{animation:bshake 2.6s ease-in-out}
@keyframes bshake{0%,100%{transform:none}16%{transform:translate(3px,-2px)}34%{transform:translate(-3px,2px)}52%{transform:translate(2px,2px)}70%{transform:translate(-2px,-1px)}}
.bt.major .flash{background:radial-gradient(circle at 50% 46%,#fffdf2,#ffe9a8 30%,color-mix(in srgb,var(--m) 55%,transparent) 58%,transparent 78%);animation-duration:3.6s}
.bt.major .ring{border-width:3px;box-shadow:0 0 44px var(--m)}
.bt.major .ring.r2{animation-delay:.35s;border-color:#fff3cf}
.bt.major .ring.r3{animation-delay:.7s;border-style:dashed}
.bt .pt{position:absolute;left:50%;top:45%;width:5px;height:5px;border-radius:50%;background:var(--pc,#ffd97a);box-shadow:0 0 8px var(--pc,#ffd97a);animation:ptfly 1.9s cubic-bezier(.15,.75,.3,1) forwards;opacity:0}
@keyframes ptfly{0%{transform:translate(0,0) scale(1.2);opacity:1}100%{transform:translate(var(--px),var(--py)) scale(.15);opacity:0}}
.bt .verdict{position:absolute;left:50%;bottom:19%;transform:translateX(-50%);text-align:center;animation:vf 1.6s .9s both;width:100%}
.bt .verdict h2{font-size:36px;letter-spacing:.42em;text-indent:.42em;color:#fff3cf;text-shadow:0 0 30px var(--m)}
.bt .verdict p{margin-top:13px;font-size:14px;letter-spacing:.34em;text-indent:.34em;color:#cabd9a}
@keyframes vf{from{opacity:0;transform:translateX(-50%) translateY(16px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
.doom{position:absolute;inset:0;display:none;z-index:4}
.doom.on{display:block}
.doom .vig{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 50%,rgba(184,69,58,.58));animation:dv 2.6s ease-out forwards}
@keyframes dv{0%{opacity:0}20%{opacity:1}100%{opacity:0}}
.doom .foe{position:absolute;right:-320px;top:14%;width:min(310px,34vw);aspect-ratio:1;object-fit:cover;border-radius:18px;border:2px solid #b8453a;box-shadow:0 0 50px rgba(184,69,58,.75);animation:fi 3.4s cubic-bezier(.2,.9,.3,1) forwards}
@keyframes fi{0%{transform:translateX(0);opacity:0}15%{opacity:1;transform:translateX(-330px)}76%{transform:translateX(-330px);opacity:1}100%{transform:translateX(0);opacity:0}}
.doom .say{position:absolute;right:calc(min(310px,34vw) + 40px);top:22%;max-width:320px;padding:13px 17px;border-radius:13px;background:rgba(11,14,21,.95);border:1px solid #b8453a;color:#e6ddc8;font-size:13.5px;line-height:1.8;animation:si 3.4s ease forwards}
.doom .say b{color:#d86a5a;display:block;margin-bottom:5px;font-size:11px;letter-spacing:.24em}
@keyframes si{0%{opacity:0;transform:translateY(8px)}13%{opacity:1;transform:none}78%{opacity:1}100%{opacity:0}}
.empty{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);text-align:center;transition:opacity .5s;pointer-events:none}
.empty .ep{width:178px;aspect-ratio:3/4;object-fit:cover;object-position:center 10%;border-radius:16px;border:1.5px solid color-mix(in srgb,var(--m) 55%,transparent);box-shadow:0 14px 60px rgba(0,0,0,.6);opacity:.95}
.empty .eq{margin-top:16px;color:#d6cde0;font-size:14.5px;letter-spacing:.3em;text-indent:.3em;text-shadow:0 2px 18px rgba(0,0,0,.85)}
.empty .ee{margin-top:8px;color:#79839a;font-size:10.5px;letter-spacing:.2em}
.gear{position:absolute;left:14px;bottom:14px;pointer-events:auto;width:28px;height:28px;border-radius:50%;border:1px solid #2a3348;background:rgba(11,14,21,.85);color:#8a93a6;font-size:13px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.gear:hover{color:var(--m);border-color:var(--m)}
.panel{position:absolute;left:14px;bottom:48px;pointer-events:auto;width:242px;padding:12px;border-radius:14px;background:rgba(11,14,21,.97);border:1px solid #2a3348;display:none}
.panel.on{display:block}
.panel h4{font-size:11px;color:#8a93a6;letter-spacing:.2em;margin-bottom:8px}
.panel select,.panel button{width:100%;margin:4px 0;padding:5px 8px;font-size:12px;background:#131926;color:#e6ddc8;border:1px solid #2a3348;border-radius:8px}
.panel button{cursor:pointer}.panel button:hover{border-color:var(--m);color:var(--m)}
.panel label{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:#aab3c6;margin-top:6px;cursor:pointer}
.panel .row{display:flex;gap:6px}
.cbook{position:absolute;left:50px;bottom:14px;pointer-events:auto;width:28px;height:28px;border-radius:50%;border:1px solid #2a3348;background:rgba(11,14,21,.85);color:#8a93a6;font-size:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;z-index:2}
.cbook:hover{color:var(--m);border-color:var(--m)}
.cron{position:absolute;top:0;right:0;bottom:0;width:min(620px,96vw);pointer-events:auto;display:none;flex-direction:column;background:linear-gradient(160deg,rgba(9,12,18,.98),rgba(13,17,27,.98));border-left:1px solid color-mix(in srgb,var(--m) 45%,transparent);box-shadow:-18px 0 60px rgba(0,0,0,.65);z-index:8}
.cron.on{display:flex}
.cron-h{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid #232c40}
.cron-h h2{font-size:15px;color:#efe6cf;letter-spacing:.3em;font-weight:400;text-shadow:0 0 24px var(--m)}
.cron-x{cursor:pointer;color:#8a93a6;font-size:11px;letter-spacing:.2em;border:1px solid #2a3348;border-radius:999px;padding:6px 18px}
.cron-x:hover{color:var(--m);border-color:var(--m)}
.cron-list{overflow-y:auto;padding:14px 16px 44px;display:flex;flex-direction:column;gap:14px;scrollbar-width:thin;scrollbar-color:#2a3348 transparent}
.ccard{position:relative;flex:none;border-radius:14px;overflow:hidden;border:1px solid #26304a;background:#0d1220}
.charge{position:absolute;inset:0;display:none;align-items:center;justify-content:center;flex-direction:column;gap:22px;pointer-events:none;z-index:9;background:rgba(4,6,10,.4);backdrop-filter:blur(2px)}
.charge.on{display:flex}
.charge .cring{width:200px;height:200px;border-radius:50%;background:conic-gradient(var(--m) 0deg,rgba(255,255,255,.09) 0deg);-webkit-mask:radial-gradient(circle,transparent 61%,#000 64%);mask:radial-gradient(circle,transparent 61%,#000 64%);box-shadow:0 0 50px color-mix(in srgb,var(--m) 45%,transparent)}
.charge .ctxt{color:#efe6cf;font-size:15px;letter-spacing:.32em;text-indent:.32em;text-shadow:0 0 22px var(--m)}
.ccard .cbg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.15;filter:saturate(.9)}
.ccredit{position:absolute;right:8px;top:8px;font-size:9px;color:#7d8698;letter-spacing:.06em;background:rgba(5,7,11,.66);padding:2px 8px;border-radius:999px;z-index:2}
.ccin{position:relative;display:flex;gap:12px;padding:12px}
.cpic{width:118px;height:158px;border-radius:10px;object-fit:cover;flex:none;border:1px solid #33405e;background:#0b0e15}
.cgly{width:118px;height:158px;border-radius:10px;flex:none;display:flex;align-items:center;justify-content:center;font-size:46px;color:var(--m);font-weight:700;text-shadow:0 0 30px var(--m);border:1.5px dashed color-mix(in srgb,var(--m) 55%,transparent);background:radial-gradient(circle at 35% 28%,rgba(255,255,255,.09),transparent)}
.ctit{font-size:14px;color:var(--m);letter-spacing:.14em;font-weight:700}
.crng{margin-left:8px;font-size:10px;color:#79839a;letter-spacing:.04em}
.cdig{margin-top:5px;color:#e6ddc8;font-size:12.5px;letter-spacing:.16em}
.cev{margin:8px 0 0}
.cev li{list-style:none;color:#aab3c6;font-size:11px;line-height:1.68;margin-bottom:3px}
.cev li b{color:#d6cde0;font-weight:600;margin-right:5px}
.ccq{margin-top:7px;color:#96a0b5;font-size:11px;letter-spacing:.06em;border-left:2px solid color-mix(in srgb,var(--m) 55%,transparent);padding-left:8px}
.cbadges{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap}
.cbadge{font-size:9.5px;color:#7d8698;border:1px solid #26304a;border-radius:999px;padding:2px 9px;letter-spacing:.08em}
`;
			shadow.appendChild(style);

			const nr = document.createElement("div");
			nr.className = "nr";
			nr.style.setProperty("--m", "#c9a55c");
			nr.style.setProperty("--a", "#5a9e8f");
			nr.innerHTML = `
<div class="hud">
  <img class="seal" alt=""><div class="bridge">桥</div>
  <div class="rt"><div class="rn"></div><div class="rs"></div></div>
  <div class="bar"><i></i><b></b></div>
  <div class="jade"><em><span class="cn"></span> <b class="jv">0</b></em><span>修行资产</span></div>
  <div class="track">真 <i class="tv">0</i><br>演 <i class="dv2">0</i></div>
</div>
<div class="empty"><img class="ep" alt=""><div class="eq"></div><div class="ee"></div></div>
<div class="comp"><button class="cmin" title="收起/展开">–</button><button class="c3d" title="3D 模式">3D</button><img alt="王林"><div class="ground"></div><div class="cname">王 林</div><div class="csub"></div></div>
<div class="v3d"><canvas></canvas><div class="ld">3D 资产加载中…</div><div class="x">收起 3D</div><div class="hint">拖拽旋转 · 滚轮缩放</div></div>
<div class="insp"><img alt=""><div class="q"></div><div class="x">收起神游</div></div>
<div class="splash"><h1>${SPLASH_LINE}</h1><p>每一次编码，都是一场修行</p><button>入　道</button></div>
<div class="bt"><video class="vid" muted playsinline></video><div class="flash"></div><div class="ring"></div><img class="newseal" alt=""><div class="glyph"></div><div class="verdict"><h2></h2><p></p></div></div>
<div class="doom"><div class="vig"></div><img class="foe" alt=""><div class="say"><b>心魔劫</b><span class="q"></span></div></div>
<button class="gear">道</button>
<div class="panel">
  <h4>逆天主题 · 控制台</h4>
  <select class="jump"></select>
  <button class="go">⚡ 入此境（演出）</button>
  <div class="row"><button class="a1">＋1M</button><button class="a2">＋1B</button><button class="a3">＋1T</button></div>
  <button class="rd">清空演示灵力（真实保留）</button>
  <label>全局音效<input type="checkbox" class="tg-audio"></label>
  <label>氛围垫底音<input type="checkbox" class="tg-amb"></label>
  <label>音量<input type="range" class="vol" min="0" max="1" step="0.05"></label>
  <label>王林陪伴<input type="checkbox" class="tg-comp"></label>
  <label>沉浸文案<input type="checkbox" class="tg-rel"></label>
  <label>全量换皮<input type="checkbox" class="tg-skin"></label>
</div>
<button class="cbook" title="逆天修行录 · 编年史卷轴">录</button>
<div class="cron"><div class="cron-h"><h2>逆天修行录 · 编年史卷轴</h2><i class="cron-x">收起卷轴</i></div><div class="cron-list"></div></div>`;
			shadow.appendChild(nr);

			const $ = (s) => shadow.querySelector(s);
			const ui = {
				seal: $(".seal"), bridge: $(".bridge"), rn: $(".rn"), rs: $(".rs"),
				fill: $(".bar>i"), barTxt: $(".bar>b"),
				cn: $(".cn"), jv: $(".jv"), tv: $(".tv"), dv: $(".dv2"),
				empty: $(".empty"), ep: $(".ep"), eq: $(".eq"), ee: $(".ee"),
				comp: $(".comp"), compImg: $(".comp img"), csub: $(".csub"),
				insp: $(".insp"), inspImg: $(".insp img"), inspQ: $(".insp .q"),
				splash: $(".splash"), bt: $(".bt"), newSeal: $(".bt .newseal"), glyph: $(".bt .glyph"),
				vH: $(".verdict h2"), vP: $(".verdict p"),
				doom: $(".doom"), foe: $(".doom .foe"), sayQ: $(".doom .say .q"),
				panel: $(".panel"), jump: $(".jump"), nv: bgHost.querySelector(".nv")
			};
			ui.jump.innerHTML = REALMS.map((r, i) => `<option value="${i}">${esc(r.name)} · ${esc(r.sub)}</option>`).join("");
			$(".tg-audio").checked = opts.audio; $(".tg-comp").checked = opts.companion;
			$(".tg-amb").checked = opts.ambient;
			$(".vol").value = parseFloat(localStorage.getItem("nitian.vol") || "0.6");
			$(".tg-rel").checked = opts.relabel; $(".tg-skin").checked = opts.skin;

			const total = () => realTokens + demoTokens();
			function subTier(r, t) {
				if (r.id === "15_kongjie") {
					const p = (t - r.from) / (r.to - r.from);
					return p < .34 ? "初期 · 金尊" : p < .67 ? "中期 · 天尊" : "圆满 · 大天尊";
				}
				const idxNow = REALMS.indexOf(r);
				if (idxNow >= 15 && r.to !== Infinity) {
					const p = (t - r.from) / (r.to - r.from);
					return p < .8 ? r.sub : "近彼岸";
				}
				return r.sub;
			}
			function paint(i) {
				const r = REALMS[i];
				nr.style.setProperty("--m", r.main);
				const de = document.documentElement;
				de.style.setProperty("--nit-m", r.main);
				de.style.setProperty("--nit-a", r.accent);
				de.style.setProperty("--nit-seal", "url(" + (r.seal || CH.ningshi) + ")");
				nr.style.setProperty("--a", r.accent);
				setBg(r.bg);
				ui.nv.style.background = `radial-gradient(ellipse at 50% 118%, ${hexA(r.main, .17)}, transparent 60%)`;
				const isBridge = i >= 18;
				if (r.seal && !isBridge) { ui.seal.src = r.seal; ui.seal.style.display = ""; ui.bridge.style.display = "none"; }
				else { ui.seal.style.display = "none"; ui.bridge.style.display = "flex"; ui.bridge.textContent = isBridge ? ["一","二","三","四","五","六","七","八","九"][i - 18] : "境"; }
				ui.rn.textContent = r.name;
				ui.rs.textContent = subTier(r, total());
				const hi = r.to === Infinity ? r.from + 5e8 : r.to;
				const pct = Math.min(100, Math.max(0, ((total() - r.from) / (hi - r.from)) * 100));
				ui.fill.style.width = pct.toFixed(1) + "%";
				ui.barTxt.textContent = fmt(total()) + " / " + fmt(hi);
				ui.cn.textContent = r.cur;
				ui.jv.textContent = fmt(total());
				ui.tv.textContent = fmt(realTokens);
				ui.dv.textContent = demoTokens() > 0 ? "+" + fmt(demoTokens()) : "0";
				if (opts.companion) {
					ui.comp.style.display = "";
					ui.compImg.src = r.char;
					ui.csub.textContent = r.name + " · " + r.cur;
				} else ui.comp.style.display = "none";
				if (opts.ambient) setAmbient(i);
				ui.ep.src = r.char;
				const crQ0 = chronOf(r.id).quotes || [];
				ui.eq.textContent = (crQ0[0] && crQ0[0].text) || QUOTES[r.id] || QUOTES.default;
				ui.ee.textContent = "论道未启 · 道音将现于此";
			}

			function enter(i, silent) {
				const prev = idx;
				idx = i;
				localStorage.setItem(LS.demo, String(Math.max(demoTokens(), REALMS[i].from - realTokens)));
				paint(idx);
				if (silent) return;
				const major = i > prev && [3, 6, 10, 18].includes(i);
				if (opts.audio) { sfxRise(); setTimeout(sfxGong, major ? 1200 : 900); }
				const r = REALMS[i];
				if (r.seal && i < 18) { ui.newSeal.src = r.seal; ui.newSeal.style.display = ""; ui.glyph.style.display = "none"; }
				else { ui.newSeal.style.display = "none"; ui.glyph.style.display = "flex"; ui.glyph.textContent = i >= 15 ? ["一","二","三","四","五","六","七","八","九"][i - 18] : "境"; }
				const crS = chronOf(r.id).scene;
				ui.vH.textContent = r.name; ui.vP.textContent = crS ? String(crS).slice(0, 46) : r.sub;
				ui.bt.classList.toggle("major", major);
				const vid = ui.bt.querySelector(".vid");
				if (major && vid) {
					const btVid = { 3: "bt_m", 6: "bt_b", 10: "bt_t", 18: "bt_p" }[i] || "bt_wanglin_face";
				vid.src = A + "/animations/" + btVid + ".mp4";
					vid.currentTime = 0;
					ui.bt.classList.add("playvid");
					vid.play().catch(() => { });
					vid.onended = () => ui.bt.classList.remove("playvid");
				}
				if (major) {
					for (let k = 0; k < 46; k++) {
						const p = document.createElement("i");
						p.className = "pt";
						const ang = Math.random() * Math.PI * 2, dist = 240 + Math.random() * 460;
						p.style.setProperty("--px", Math.cos(ang) * dist + "px");
						p.style.setProperty("--py", Math.sin(ang) * dist + "px");
						p.style.setProperty("--pc", ["#ffd97a", "#7fe0d0", "#fff3cf", "#8fb7ff"][k % 4]);
						p.style.animationDelay = (Math.random() * 0.9).toFixed(2) + "s";
						ui.bt.appendChild(p);
						setTimeout(() => p.remove(), 3400);
					}
				}
				ui.bt.classList.add("on");
				setTimeout(() => { ui.bt.classList.remove("on", "major", "playvid"); [...ui.bt.querySelectorAll(".pt")].forEach(x => x.remove()); try { vid.pause(); } catch { } }, major ? 7600 : 4300);
			}

			function doom() {
				const now = Date.now();
				if (now - lastErrorAt < 9000) return;
				lastErrorAt = now;
				const rr = REALMS[idx];
				if (opts.audio) sfxDoom();
				const crQ = chronOf(rr.id).quotes || [];
				ui.sayQ.textContent = (crQ.length ? crQ[Math.floor(Math.random() * crQ.length)].text : "") || QUOTES[rr.id] || QUOTES.default;
				if (rr.enemy) { ui.foe.src = rr.enemy; ui.foe.style.display = ""; } else ui.foe.style.display = "none";
				ui.doom.classList.add("on");
				setTimeout(() => ui.doom.classList.remove("on"), 3500);
			}

			$(".splash button").addEventListener("click", () => { ui.splash.classList.add("off"); sessionStorage.setItem(LS.seen, "1"); if (opts.audio) sfxGong(); });
			if (sessionStorage.getItem(LS.seen)) ui.splash.classList.add("off");
			// 立牌：拖拽 + 收起 + 点按神游（拖拽阈值 6px 区分点按）
			const compPos = (() => { try { return JSON.parse(localStorage.getItem("nitian.compPos") || "null"); } catch { return null; } })();
			if (compPos && compPos.left && compPos.top) {
				ui.comp.style.left = compPos.left; ui.comp.style.top = compPos.top;
				ui.comp.style.right = "auto"; ui.comp.style.bottom = "auto";
			}
			let dragging = false, moved = 0, dx = 0, dy = 0;
			ui.comp.addEventListener("pointerdown", (e) => {
				if (e.target.closest(".cmin")) return;
				const r = ui.comp.getBoundingClientRect();
				ui.comp.style.left = r.left + "px"; ui.comp.style.top = r.top + "px";
				ui.comp.style.right = "auto"; ui.comp.style.bottom = "auto";
				dx = e.clientX - r.left; dy = e.clientY - r.top;
				moved = 0; dragging = true;
				ui.comp.classList.add("dragging");
				ui.comp.setPointerCapture(e.pointerId);
			});
			ui.comp.addEventListener("pointermove", (e) => {
				if (!dragging) return;
				const x = Math.min(innerWidth - 60, Math.max(0, e.clientX - dx));
				const y = Math.min(innerHeight - 60, Math.max(0, e.clientY - dy));
				moved += Math.abs(e.movementX) + Math.abs(e.movementY);
				ui.comp.style.left = x + "px"; ui.comp.style.top = y + "px";
			});
			ui.comp.addEventListener("pointerup", () => {
				if (!dragging) return;
				dragging = false;
				ui.comp.classList.remove("dragging");
				try { localStorage.setItem("nitian.compPos", JSON.stringify({ left: ui.comp.style.left, top: ui.comp.style.top })); } catch { }
				if (moved < 6) {
					ui.inspImg.src = REALMS[idx].char;
					ui.inspQ.textContent = QUOTES[REALMS[idx].id] || QUOTES.default;
					ui.insp.classList.add("on");
				}
			});
			let v3dInit = false, v3dStop = null, v3dLoadedModel = "";
			const v3dModelFor = (rid) => {
				const n = parseInt(rid, 10);
				if (n >= 6 && n <= 8) return A + "/ui/models/nianfan2.glb";
				if (n >= 9) return A + "/ui/models/movie1.glb";
				return A + "/ui/models/wanglin_3d.glb";
			};
			async function open3D() {
				const ov = $(".v3d"); ov.classList.add("on");
				const cv = ov.querySelector("canvas"), ld = ov.querySelector(".ld");
				ld.style.display = ""; ld.textContent = "3D 资产加载中…";
				try {
				if (!v3dInit) {
					const asModule = async (path) => {
						const txt = await (await fetch(path)).text();
						return URL.createObjectURL(new Blob([txt], { type: "application/javascript" }));
					};
					const mk = async (path, repl) => {
						let txt = await (await fetch(path)).text();
						for (const [spec, url] of Object.entries(repl)) {
							txt = txt.split("'" + spec + "'").join("'" + url + "'");
							txt = txt.split('"' + spec + '"').join('"' + url + '"');
						}
						return URL.createObjectURL(new Blob([txt], { type: "application/javascript" }));
					};
					const threeUrl = await asModule(A + "/ui/vendor/three.module.js");
					const bufUrl = await mk(A + "/ui/vendor/addons/utils/BufferGeometryUtils.js", { three: threeUrl });
					const gltfUrl = await mk(A + "/ui/vendor/addons/loaders/GLTFLoader.js", { three: threeUrl, "../utils/BufferGeometryUtils.js": bufUrl, "../three.module.js": threeUrl });
					const orbUrl = await mk(A + "/ui/vendor/addons/controls/OrbitControls.js", { three: threeUrl });
					const { GLTFLoader } = await import(gltfUrl);
					const { OrbitControls } = await import(orbUrl);
					const THREE = await import(threeUrl);
					const renderer = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true });
					const scene = new THREE.Scene();
					const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
					camera.position.set(0, 0.6, 3.2);
					scene.add(new THREE.AmbientLight(0xffffff, 1.1));
					const key = new THREE.DirectionalLight(0xfff2d0, 2.2); key.position.set(3, 5, 4); scene.add(key);
					const rim = new THREE.DirectionalLight(0x7fb2e8, 1.4); rim.position.set(-4, 2, -3); scene.add(rim);
					const loader = new GLTFLoader();
					const wantModel = v3dModelFor(REALMS[idx].id);
					if (v3dLoadedModel && v3dLoadedModel !== wantModel) {
						scene.clear();
						scene.add(new THREE.AmbientLight(0xffffff, 1.1));
						const k2 = new THREE.DirectionalLight(0xfff2d0, 2.2); k2.position.set(3, 5, 4); scene.add(k2);
						const r2 = new THREE.DirectionalLight(0x7fb2e8, 1.4); r2.position.set(-4, 2, -3); scene.add(r2);
					}
					v3dLoadedModel = wantModel;
					loader.load(wantModel, (g) => {
						const m = g.scene;
						const box = new THREE.Box3().setFromObject(m);
						const size = box.getSize(new THREE.Vector3()), ctr = box.getCenter(new THREE.Vector3());
						const s = 2.2 / Math.max(size.x, size.y, size.z);
						m.scale.setScalar(s);
						m.position.sub(ctr.multiplyScalar(s));
						m.rotation.y = 0.4;
						scene.add(m);
						ld.style.display = "none";
					}, (ev) => { if (ev.total) ld.textContent = "3D 资产加载中… " + Math.round(ev.loaded / ev.total * 100) + "%"; });
					const ctl = new OrbitControls(camera, cv);
					ctl.autoRotate = true; ctl.autoRotateSpeed = 2.2; ctl.enableDamping = true;
					let alive = true;
					(function loop() { if (!alive) return; requestAnimationFrame(loop); ctl.update(); renderer.render(scene, camera); })();
					const fit = () => { const w = ov.clientWidth, hh = ov.clientHeight; renderer.setSize(w, hh, false); camera.aspect = w / hh; camera.updateProjectionMatrix(); };
					fit(); window.addEventListener("resize", fit);
					v3dStop = () => { alive = false; window.removeEventListener("resize", fit); };
					v3dInit = true;
				}
				} catch (e) {
					const ld = document.querySelector("#nitian-host").shadowRoot.querySelector(".v3d .ld");
					if (ld) { ld.style.display = ""; ld.textContent = "3D-ERR: " + String(e && e.message ? e.message : e).slice(0, 170); }
				}
			}
			$(".c3d").addEventListener("click", (e) => { e.stopPropagation(); open3D(); });
			$(".v3d .x").addEventListener("click", () => { $(".v3d").classList.remove("on"); if (v3dStop) v3dStop(); });
			$(".cmin").addEventListener("click", (e) => {
				e.stopPropagation();
				ui.comp.classList.toggle("mini");
				localStorage.setItem("nitian.compMini", ui.comp.classList.contains("mini") ? "1" : "0");
			});
			if (localStorage.getItem("nitian.compMini") === "1") ui.comp.classList.add("mini");
			$(".insp .x").addEventListener("click", () => ui.insp.classList.remove("on"));
			$(".gear").addEventListener("click", () => ui.panel.classList.toggle("on"));
			$(".go").addEventListener("click", () => { enter(parseInt(ui.jump.value)); ui.panel.classList.remove("on"); });
			const addDemo = (d) => {
				const before = idx;
				localStorage.setItem(LS.demo, String(demoTokens() + d));
				idx = realmOf(total());
				paint(idx);
				if (idx > before) enter(idx);
			};
			$(".a1").addEventListener("click", () => addDemo(1e6));
			$(".a2").addEventListener("click", () => addDemo(1e9));
			$(".a3").addEventListener("click", () => addDemo(1e12));
			$(".rd").addEventListener("click", () => { localStorage.setItem(LS.demo, "0"); idx = realmOf(total()); paint(idx); ui.panel.classList.remove("on"); });
			$(".tg-audio").addEventListener("change", (e) => { opts.audio = e.target.checked; saveOpts(opts); });
			$(".tg-amb").addEventListener("change", (e) => { opts.ambient = e.target.checked; saveOpts(opts); if (!e.target.checked) setAmbient(0); else setAmbient(idx); });
			$(".vol").addEventListener("input", (e) => setVolume(parseFloat(e.target.value)));
			$(".tg-comp").addEventListener("change", (e) => { opts.companion = e.target.checked; saveOpts(opts); paint(idx); });
			$(".tg-skin").addEventListener("change", (e) => { opts.skin = e.target.checked; saveOpts(opts); location.reload(); });
			$(".tg-rel").addEventListener("change", (e) => { opts.relabel = e.target.checked; saveOpts(opts); location.reload(); });

			const errRe = /(error|failed|exception|错误|失败|异常)/i;
			new MutationObserver((muts) => {
				for (const m of muts) for (const n of m.addedNodes) {
					if (n.nodeType !== 1) continue;
					const cls = typeof n.className === "string" ? n.className : "";
					if (/error|fail/i.test(cls)) return doom();
					const t = (n.textContent || "").slice(0, 380);
					if (t && errRe.test(t)) return doom();
				}
			}).observe(document.body, { childList: true, subtree: true });

			if (opts.relabel) new MutationObserver(() => {
				const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
				let node, c = 0;
				while ((node = walker.nextNode()) && c < 40) {
					const raw = node.nodeValue.trim();
					if (!raw || raw.length > 30) continue;
					for (const [re, rep] of RELABEL) if (re.test(raw)) { node.nodeValue = node.nodeValue.replace(re, rep); c++; break; }
				}
			}).observe(document.body, { childList: true, subtree: true, characterData: true });

			// empty-state 显隐：centerCol 有实质对话时隐藏
			setInterval(() => {
				const col = document.querySelector('div[class*="_centerCol"]');
				if (!col) { ui.empty.style.opacity = "0"; return; }
				const busy = (col.innerText || "").trim().length > 260;
				ui.empty.style.opacity = busy || !opts.companion ? "0" : ".96";
			}, 1500);

			// 编年史彩蛋（assets/ui/chronicle.json）
			let CHRON = {};
			const chronAlias = { "15_kongjin":"15_kongjie","16_kongzun":"15_kongjie","17_kongyue":"15_kongjie","18_kongda":"15_kongjie","19_qiao1":"16_qiao1","20_qiao2":"17_qiao2","21_qiao3":"18_qiao3","22_qiao4":"19_qiao4","23_qiao5":"20_qiao5","24_qiao6":"21_qiao6","25_qiao7":"22_qiao7","26_qiao8":"23_qiao8","27_qiao9":"24_qiao9" };
			const chronOf = (rid) => CHRON[chronAlias[rid] || rid] || {};			fetch(A + "/ui/chronicle.json").then(r => r.ok ? r.json() : null).then(j => {
				if (j && j.realms) { CHRON = j.realms; const q0 = (chronOf(REALMS[idx].id).quotes || [])[0]; if (q0 && q0.text) ui.eq.textContent = q0.text; }
			}).catch(() => { });
			setInterval(() => {
				const cr = chronOf(REALMS[idx].id);
				if (!cr || !cr.eggs || !cr.eggs.length) return;
				const t = $(".eggtoast"); if (!t) return;
				t.querySelector(".t").textContent = cr.eggs[Math.floor(Math.random() * cr.eggs.length)];
				t.classList.add("on");
				setTimeout(() => t.classList.remove("on"), 7000);
			}, 100000);

			// 编年史卷轴（配图版，assets/ui/chronicle-img/index.json）
			let CIMGS = {};
			fetch(A + "/ui/chronicle-img/index.json").then(r => r.ok ? r.json() : null).then(j => { if (j) CIMGS = j; }).catch(() => { });
			const cronEl = $(".cron"), cronList = $(".cron-list");
			function picFor(r, i) {
				const m = CIMGS[r.id];
				if (!m || !m.src) {
					const g = m && m.glyph ? m.glyph : "境";
					return `<div class="cgly">${g}</div>`;
				}
				return `<img class="cpic" loading="lazy" src="${A}${m.src}" alt="">`;
			}
			function openChron() {
				try {
					cronList.innerHTML = REALMS.map((r, i) => {
					const cr = chronOf(r.id);
					const evs = cr.events || [], qs = cr.quotes || [], eggs = cr.eggs || [];
					const m = CIMGS[r.id] || {};
					const hi = r.to === Infinity ? "∞" : fmt(r.to);
					const evHtml = evs.slice(0, 3).map(e => `<li><b>${esc(e.title)}</b>${esc(String(e.summary || "").slice(0, 60))}</li>`).join("");
					const q = qs.length ? esc(qs[Math.floor(Math.random() * qs.length)].text) : "";
					return `<div class="ccard">
					<img class="cbg" loading="lazy" src="${r.bg}" alt="">
					${m.credit ? `<span class="ccredit">${esc(m.credit)}</span>` : ""}
					<div class="ccin">
						${picFor(r, i)}
						<div>
							<div><span class="ctit">${esc(r.name)}</span><span class="crng">道行 ${fmt(r.from)} ～ ${hi}</span></div>
							<div class="cdig">${esc(m.digest || r.sub)}</div>
							<ul class="cev">${evHtml}</ul>
							${q ? `<div class="ccq">${q}</div>` : ""}
							<div class="cbadges"><span class="cbadge">彩蛋 ×${eggs.length}</span>${cr.scene ? `<span class="cbadge">名场面</span>` : ""}${evs.length ? `<span class="cbadge">大事记 ×${evs.length}</span>` : ""}${qs.length ? `<span class="cbadge">语录 ×${qs.length}</span>` : ""}</div>
						</div>
					</div></div>`;
				}).join("");
					cronEl.classList.add("on");
					cronList.scrollTop = 0;
				} catch (e) { console.warn("[nitian] 卷轴渲染失败", e); }
			}
			$(".cbook").addEventListener("click", openChron);
			$(".cron-x").addEventListener("click", () => cronEl.classList.remove("on"));
			addEventListener("keydown", (e) => { if (e.key === "Escape") cronEl.classList.remove("on"); });

			// 交互示例：长按境界印蓄力破境（松手触发破境演出到下一境）
			const chargeEl = document.createElement("div");
			chargeEl.className = "charge";
			chargeEl.innerHTML = `<div class="cring"></div><div class="ctxt">蓄力破境</div>`;
			nr.appendChild(chargeEl);
			const chgRing = chargeEl.querySelector(".cring"), chgTxt = chargeEl.querySelector(".ctxt");
			const chg = { on: false, p: 0, raf: 0, t0: 0 };
			function chgStep() {
				if (!chg.on) return;
				chg.p = Math.min(1, (performance.now() - chg.t0) / 1400);
				chgRing.style.background = `conic-gradient(var(--m) ${chg.p * 360}deg, rgba(255,255,255,.09) 0deg)`;
				chgTxt.textContent = chg.p >= 1 ? "松开 · 破境！" : "蓄力破境 " + Math.floor(chg.p * 100) + "%";
				chg.raf = requestAnimationFrame(chgStep);
			}
			function chgStart(e) {
				if (cronEl.classList.contains("on")) return;
				e.preventDefault();
				chg.on = true; chg.t0 = performance.now();
				chargeEl.classList.add("on");
				chg.raf = requestAnimationFrame(chgStep);
			}
			function chgEnd() {
				if (!chg.on) return;
				chg.on = false; cancelAnimationFrame(chg.raf);
				if (chg.p >= 1 && idx < REALMS.length - 1) {
					chargeEl.classList.remove("on");
					const next = idx + 1;
					localStorage.setItem(LS.demo, String(Math.max(demoTokens(), REALMS[next].from - realTokens)));
					enter(next);
				} else if (chg.p > 0.15) {
					chgTxt.textContent = "蓄力未满";
					setTimeout(() => chargeEl.classList.remove("on"), 800);
				} else chargeEl.classList.remove("on");
				chg.p = 0;
			}
			ui.seal.addEventListener("pointerdown", chgStart);
			ui.bridge.addEventListener("pointerdown", chgStart);
			addEventListener("pointerup", chgEnd);
			addEventListener("pointercancel", chgEnd);

			async function poll() {
				try {
					const res = await fetch("/api/nitian/usage");
					const j = await res.json();
					if (j && j.ok && typeof j.real.total === "number") {
						realTokens = j.real.total;
						const ni = realmOf(total());
						if (idx < 0) { idx = ni; paint(idx); }
						else if (ni > idx) enter(ni);
						else if (ni !== idx) { idx = ni; paint(idx); }
						else paint(idx);
					}
				} catch { }
			}
			poll();
			setInterval(poll, 30000);

			idx = realmOf(total());
			paint(idx);
			console.log("[nitian] 引擎 v2.3 启动 ·", REALMS[idx].name, "· 真实修为", realTokens);
			exports.api = { enter, doom, addDemo, realms: REALMS, poll, openChron };
		}
		//#endregion

		exports.apply = apply;
		exports.inject = [];
		return module.exports;
	}
});
