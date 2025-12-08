export default function BlogPosts({ posts }) {
  return posts.map(post => <BlogPost key={post.id} post={post} />)
}

export async function genesisStaticProps() {
  const posts = await getBlogPosts();
  return {
    props: {posts}
  }
}
