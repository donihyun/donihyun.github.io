const { Component, Fragment } = require('inferno');

module.exports = class extends Component {
    render() {
        return <Fragment>
            <div class="a2a_kit a2a_kit_size_32 a2a_default_style">
                <a class="a2a_dd" href="https://www.addtoany.com/share" aria-label="More sharing options"></a>
                {['x', 'linkedin', 'email', 'facebook', 'wechat', 'line', 'telegram', 'blogger'].map(service =>
                    <a class={`a2a_button_${service}`} aria-label={`Share via ${service}`}></a>)}
            </div>
            <script defer src="https://static.addtoany.com/menu/page.js"></script>
        </Fragment>;
    }
};
