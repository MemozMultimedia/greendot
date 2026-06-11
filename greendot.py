import os
import base64
import requests
import streamlit as st

GITHUB_REPO = os.environ.get('GITHUB_REPO', 'MemozMultimedia/greendot')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
API_BASE = 'https://api.github.com'

HEADERS = {
    'Accept': 'application/vnd.github.v3+json'
}
if GITHUB_TOKEN:
    HEADERS['Authorization'] = f'token {GITHUB_TOKEN}'


def fetch_github(path):
    url = f'{API_BASE}/{path}'
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 404:
        st.error('Repositorio no encontrado. Verifica `GITHUB_REPO` y tu token.')
        st.stop()
    if resp.status_code == 401:
        st.error('Autenticación fallida. Revisa tu `GITHUB_TOKEN`.')
        st.stop()
    resp.raise_for_status()
    return resp.json()


def list_repo_contents(path=''):
    data = fetch_github(f'repos/{GITHUB_REPO}/contents/{path}')
    if isinstance(data, dict):
        return [data]
    return sorted(data, key=lambda item: (item['type'], item['name']))


def get_readme():
    data = fetch_github(f'repos/{GITHUB_REPO}/readme')
    content = base64.b64decode(data['content']).decode('utf-8')
    return content


def get_file_content(path):
    data = fetch_github(f'repos/{GITHUB_REPO}/contents/{path}')
    if data.get('encoding') == 'base64':
        return base64.b64decode(data['content']).decode('utf-8')
    return ''


def main():
    st.set_page_config(page_title='GreenDot GitHub Viewer', layout='wide')
    st.title('Visualizador del repositorio GreenDot')
    st.markdown(
        'Este Streamlit conecta con GitHub para leer el repositorio ' +
        f'**{GITHUB_REPO}** y mostrar su README, archivos y detalles.'
    )

    if not GITHUB_TOKEN:
        st.warning('No se ha proporcionado `GITHUB_TOKEN`. El acceso a repositorios privados y la tasa de consultas será limitada.')

    st.sidebar.header('Configuración')
    st.sidebar.markdown(f'- **Repositorio:** `{GITHUB_REPO}`')
    token_status = 'Sí' if GITHUB_TOKEN else 'No'
    st.sidebar.markdown(f'- **Token activo:** {token_status}')

    with st.expander('README del repositorio'):
        readme = get_readme()
        st.markdown(readme)

    st.sidebar.header('Explorador de archivos')
    folder = st.sidebar.text_input('Ruta de carpeta', '')
    contents = list_repo_contents(folder)

    st.sidebar.markdown('### Contenido')
    for item in contents:
        icon = '📁' if item['type'] == 'dir' else '📄'
        st.sidebar.write(f"{icon} {item['name']}")

    st.markdown('## Contenido del repositorio')
    cols = st.columns([3, 1, 1])
    cols[0].markdown('**Nombre**')
    cols[1].markdown('**Tipo**')
    cols[2].markdown('**Tamaño**')

    for item in contents:
        cols = st.columns([3, 1, 1])
        cols[0].markdown(item['name'])
        cols[1].markdown(item['type'])
        cols[2].markdown(f"{item.get('size', 0)} bytes")

    selected_file = st.selectbox('Selecciona un archivo para previsualizar', [item['path'] for item in contents if item['type'] == 'file'])
    if selected_file:
        content = get_file_content(selected_file)
        if selected_file.lower().endswith(('.md', '.txt', '.json', '.js', '.php', '.py', '.html', '.css')):
            st.code(content, language=selected_file.split('.')[-1])
        else:
            st.text(content)


if __name__ == '__main__':
    main()
