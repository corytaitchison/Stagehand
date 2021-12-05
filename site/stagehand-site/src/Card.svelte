<script lang="ts">
    export let rotation: number = 3;
</script>

<div class="card" style="--rotation: {rotation}deg;">
    <slot></slot>
</div>

<style>
    .card {
        background-color: white; 
        margin: 0 5vw 15vh 5vw; 
        border-radius: 5vw; 
        padding: 3rem;
        color:  black;
        box-shadow: 3px 3px 30px rgba(0,0,0,0.7);
        transform:  rotate(var(--rotation));
    }

    @media screen and (max-width: 500px) {
        .card {
            margin: 15vh 0;
            border-radius: 0;
            transform:  none;
            font-size: 1.5rem;
            transform:  none;
        }
    }
</style>