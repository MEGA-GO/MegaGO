<template>
    <v-card class="profile-card">
        <div class="profile-card_cover">
            <img src="./../assets/abstract_background.png" alt="profile background">
        </div>
        <div class="profile-card_padding">
            <div class="profile-card_image">
                <img :src="profilePicture" alt="profile picture">
            </div>
            <div class="profile-card_details">
                <h3>{{ name }}</h3>
                <p class="text-muted">{{ affiliation }}</p>
            </div>
        </div>
    </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

@Component
export default class TeamCard extends Vue {
    @Prop({ required: true })
    private name: string;

    @Prop({ required: true })
    private affiliation: string;

    @Prop({ required: false, default: require("./../assets/profile_picture.jpg") })
    private profilePicture: string;
}
</script>

<style scoped>
    .profile-card {
        background: #fff;
        -webkit-box-shadow: 0 2px 30px rgba(0, 0, 0, 0.1);
        box-shadow: 0 2px 30px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 30px;
    }

    .profile-card .profile-card_cover {
        height: 130px;
        overflow: hidden;
    }

    .profile-card .profile-card_cover img {
        width: 100%;
        height: 100%;
        -o-object-fit: cover;
        object-fit: cover;
    }

    .profile-card .profile-card_padding {
        padding: 25px;
        position: relative;
        margin-top: -85px;
    }

    .profile-card .profile-card_image {
        width: 125px;
        height: 125px;
        border-radius: 125px;
        overflow: hidden;
        border: 4px solid #fff;
        margin: 0 auto 15px auto;
        -webkit-box-shadow: 0 5px 30px rgba(0, 0, 0, 0.1);
        box-shadow: 0 5px 30px rgba(0, 0, 0, 0.1);
    }

    .profile-card .profile-card_image img {
        width: 100%;
        height: 100%;
    }

    .profile-card .profile-card_details h3 {
        font-size: 21px;
    }

    .profile-card .profile-card_details p {
        font-size: 16px;
        margin-bottom: 15px;
    }

    .profile-card .profile-card_social {
        text-align: center;
    }

    .profile-card .profile-card_social a {
        display: inline-block;
    }

    .profile-card .profile-card_social img {
        width: 33px;
        margin: 5px 10px;
    }
</style>
