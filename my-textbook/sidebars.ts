import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    'ros2-basics',
    'urdf-models',
    'digital-twins',
    'nvidia-isaac',
    'vla-models',
    'humanoid-kinematics',
    'motion-planning',
    'capstone-project',
    {
      type: 'category',
      label: 'Tutorial - Basics',
      items: [
        'tutorial-basics/create-a-document',
        'tutorial-basics/create-a-blog-post',
        'tutorial-basics/create-a-page',
        'tutorial-basics/deploy-your-site',
        'tutorial-basics/congratulations',
      ],
    },
    {
        type: 'category',
        label: 'Tutorial - Extras',
        items: [
            'tutorial-extras/manage-docs-versions',
            'tutorial-extras/translate-your-site',
        ]
    }
  ],
};

export default sidebars;
