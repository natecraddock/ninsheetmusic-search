<script>
	export let sheet;
</script>

<li>
	<span><strong>{sheet.title}</strong> by <em>{sheet.arranger}</em></span>
	<span>[{sheet.platform}] {sheet.game}</span>
	<span>Download: <a href={sheet.pdf}>pdf</a> <a href={sheet.midi}>midi</a> <a href={sheet.finale}>finale</a></span>
</li>

<style>
li {
	display: flex;
	flex-direction: column;
	margin-bottom: 1em;
}

a {
	color: #d63879;
}
</style>
