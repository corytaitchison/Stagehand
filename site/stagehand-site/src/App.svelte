<script lang="ts">
	import Icon from 'svelte-awesome';
	import { chevronDown, download, bars, github } from 'svelte-awesome/icons';
	import { fade } from 'svelte/transition';

	import Card from './Card.svelte';

	let y: number;
	let scaling: number = 50;
	let offset: string;
	let fontSize: string;
	let leftPad: string;

	const yToOne = (y: number) => Math.min(Math.max(y - 50, 0) / 300, 1);

	$: {
		// y = $yTween;
		offset = `max(-2.8em, calc(-5em + ${scaling * (1 - 0.8 * yToOne(y))}vw))`;
		fontSize = `min(calc(${(1 - yToOne(y)) * 3 + 1}rem + 2vw), 8em)`;
		leftPad = `calc(1em + ${(1 - yToOne(y)) * 20}vw - ${(1 - yToOne(y)) * 5}vh)`;
	}
</script>

<main>
	<div style="height: 40vh" />
	<div
		id="title-art"
		style="
			--offset: {offset}; 
			--bgColor: rgba(55,55,55, {yToOne(y)}); 
			--fontSize: {fontSize};
			--leftPad:  {leftPad};
			--textColor:  rgb({255 - yToOne(y) * 200}, {255 - yToOne(y) * 200}, {255 - yToOne(y) * 200});
		"
	>
		<div id="title-art-grida">stagehandstagehandstagehand</div>
		<div id="title-art-grid1"><b>stage</b></div>
		<div id="title-art-gridb">handstagehandstagehandstagehandstagehandstagehandstagehandstagehand</div>
		<div class="row2" id="title-art-gridc">handstagehandstagehandstage</div>
		<div class="row2" id="title-art-grid2"><b>hand</b></div>
		<div class="row2" id="title-art-gridd">stagehandstagehandstagehandstagehandstagehandstagehandstagehand</div>
		{#if yToOne(y) == 1}
			<div id="menuBar" transition:fade>
				<a href="/#">
					<Icon data={github} scale={2}/>
				</a>
				<button on:click={() => alert(1)}>
					<Icon data={download} scale={2}/>
				</button>
				<button on:click={() => alert(1)}>
					<Icon data={bars} scale={2}/>
				</button>

			</div>
		{/if}
	</div>
	<div style="height: 40vh; padding-top: 18vh; color: rgba(255, 255, 255,{0.5 - yToOne(y)});">
			<span on:click={() => window.scrollTo({top: 450, left: 0, behavior: "smooth"})}>
				<Icon data={chevronDown} scale={3}/>
			</span>
	</div>
	<Card> 
		<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras nibh urna, eleifend non iaculis nec, finibus non ante. Aenean aliquet enim lectus, eu gravida felis auctor in. Maecenas dapibus magna id nisi aliquet tincidunt eu pharetra lacus. Mauris id porttitor ligula. Cras vel augue ullamcorper, pretium diam ut, pulvinar turpis. Pellentesque ligula eros, dignissim nec libero vel, porttitor porttitor arcu. Nunc vitae diam quam. Etiam imperdiet, felis vel aliquam feugiat, dui dui malesuada urna, non placerat tortor nisi at urna. Morbi pellentesque urna non tristique sagittis. Morbi fringilla ex nec maximus ultrices. Sed venenatis diam at risus tempus egestas. Cras elementum feugiat tincidunt. Ut at neque eu nisi venenatis viverra. Proin cursus euismod orci in auctor. Duis in nibh dolor.</p>
	</Card>

	<Card rotation={-3}> 
		<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras nibh urna, eleifend non iaculis nec, finibus non ante. Aenean aliquet enim lectus, eu gravida felis auctor in. Maecenas dapibus magna id nisi aliquet tincidunt eu pharetra lacus. Mauris id porttitor ligula. Cras vel augue ullamcorper, pretium diam ut, pulvinar turpis. Pellentesque ligula eros, dignissim nec libero vel, porttitor porttitor arcu. Nunc vitae diam quam. Etiam imperdiet, felis vel aliquam feugiat, dui dui malesuada urna, non placerat tortor nisi at urna. Morbi pellentesque urna non tristique sagittis. Morbi fringilla ex nec maximus ultrices. Sed venenatis diam at risus tempus egestas. Cras elementum feugiat tincidunt. Ut at neque eu nisi venenatis viverra. Proin cursus euismod orci in auctor. Duis in nibh dolor.</p>
	</Card>
</main>

<svelte:window bind:scrollY="{y}" />

<style>
	main {
		text-align: center;
		padding: 0;
		margin: 0 auto;
		font-size: 2em;
	}

	#title-art {
		position: -webkit-sticky;
		position: sticky;
		top: 0;
		margin: 0;
		padding: 0;
		width: 100vw;
		overflow: hidden;
		background-color: var(--bgColor);
		z-index: 10;

		-webkit-user-select: none;  /* Chrome all / Safari all */
		-moz-user-select: none;     /* Firefox all */
		-ms-user-select: none;      /* IE 10+ */
		user-select: none;    
		cursor: default;

		color: var(--textColor);
		text-transform: lowercase;
		font-weight: 300;
		font-size: var(--fontSize);

		display: grid;
		grid-template:
			"a title1 b b" 1em
			"c c title2 d" 1.3em /
			var(--leftPad) 2.8em 2.5em auto;
		gap: 0vh 0;
	}

	#title-art .row2 {
		position: relative;
		left: var(--offset);
	}

	#title-art-grida {
		grid-area: a;
		justify-self: end;
	}

	#title-art-gridb {
		grid-area: b;
		justify-self: start;
	}

	#title-art-gridc {
		grid-area: c;
		justify-self: end;
	}

	#title-art-gridd {
		grid-area: d;
		justify-self: start;
	}

	#title-art-grid1 {
		grid-area: title1;
	}

	#title-art-grid2 {
		grid-area: title2;
	}

	b {
		font-weight: 900;
		color: #aff;
	}

	#menuBar {
		position: absolute;
		right:  1em;
		top: 25%;
		color: white;
		cursor: pointer;
	}

	#menuBar button,
	#menuBar a {
		padding:  0 1rem;
		margin:  0;
		color: white;
		background: none;
		border:  none;
		cursor:  pointer;
	}

	#menuBar button:active
	#menuBar a:active {
		color:  #aff;
	}
</style>
