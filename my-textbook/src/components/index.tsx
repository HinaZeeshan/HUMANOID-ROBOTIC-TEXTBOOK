import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Spec-Driven Book Creation',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        This textbook is built using a Spec-Driven workflow powered by
        Spec-Kit Plus and Claude Code. You define, refine, and generate
        structured content with consistency across chapters and modules.
      </>
    ),
  },

  {
    title: 'Physical AI & Humanoid Robotics Curriculum',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        The content covers core areas such as Physical AI, Embodied Intelligence,
        Humanoid Locomotion, Robot Perception, Actuators, Motion Planning, and
        real-world engineering practices for teaching next-generation robotics.
      </>
    ),
  },

  {
    title: 'Modern Tech Stack for Deployment',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Built using React and Docusaurus, the entire textbook is modular,
        version-controlled, and deployed seamlessly to GitHub Pages. Extend or
        customize your layout with React components while keeping content clean
        and maintainable.
      </>
    ),
  },
];

function Feature({ title, Svg, description }: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}











